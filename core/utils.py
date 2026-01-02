import csv
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

from django.conf import settings
from django.core.files import File
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class BulkImportProcessor:
    """Process bulk import from zip file containing CSVs and images"""
    
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.temp_dir = None
        self.errors = []
        self.stats = {
            'clients_created': 0,
            'clients_updated': 0,
            'projects_created': 0,
            'projects_updated': 0,
            'gallery_images_created': 0,
            'gallery_images_updated': 0,
        }
    
    def process(self) -> Tuple[bool, Dict, List[str]]:
        """
        Process the zip file and import data
        Returns: (success, stats, errors)
        """
        try:
            # Extract zip file
            self.temp_dir = self._extract_zip()
            
            # Validate zip structure
            if not self._validate_zip_structure():
                return False, self.stats, self.errors
            
            # Import in order: Clients -> Projects -> Gallery Images (auto-inferred)
            self._import_clients()
            self._import_projects()
            self._import_gallery_images_from_folders()
            
            # Update cover images for projects (use first image)
            self._update_project_cover_images()
            
            success = len(self.errors) == 0
            return success, self.stats, self.errors
            
        except Exception as e:
            self.errors.append(f"Critical error: {str(e)}")
            return False, self.stats, self.errors
        finally:
            # Clean up temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
    
    def _validate_zip_structure(self) -> bool:
        """Validate that zip has required structure"""
        validation_errors = []
        
        # Check for required CSV files (only clients and projects now)
        required_csvs = ['clients.csv', 'projects.csv']
        for csv_file in required_csvs:
            csv_path = self._find_file(csv_file)
            if not csv_path:
                validation_errors.append(f"❌ Missing required file: {csv_file}")
            else:
                # Validate CSV headers
                validation_errors.extend(self._validate_csv_headers(csv_path, csv_file))
        
        # If CSVs are missing, stop here
        if validation_errors:
            self.errors.extend(validation_errors)
            return False
        
        # Validate CSV content
        validation_errors.extend(self._validate_csv_content())
        
        if validation_errors:
            self.errors.extend(validation_errors)
            return False
        
        return True
    
    def _validate_csv_headers(self, csv_path: str, csv_filename: str) -> List[str]:
        """Validate that CSV has required headers"""
        errors = []
        
        required_headers = {
            'clients.csv': ['client_name'],
            'projects.csv': ['project_name', 'city', 'project_description', 'expertise', 'year'],
        }
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                if not headers:
                    errors.append(f"❌ {csv_filename}: CSV file is empty or has no headers")
                    return errors
                
                # Check for required headers
                missing_headers = []
                for required_header in required_headers.get(csv_filename, []):
                    if required_header not in headers:
                        missing_headers.append(required_header)
                
                if missing_headers:
                    errors.append(
                        f"❌ {csv_filename}: Missing required columns: {', '.join(missing_headers)}"
                    )
        except Exception as e:
            errors.append(f"❌ {csv_filename}: Error reading file - {str(e)}")
        
        return errors
    
    def _validate_csv_content(self) -> List[str]:
        """Validate CSV content for consistency"""
        errors = []
        
        # Collect client names from clients.csv
        client_names = set()
        clients_csv_path = self._find_file('clients.csv')
        if clients_csv_path:
            try:
                with open(clients_csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row_num, row in enumerate(reader, start=2):
                        client_name = row.get('client_name', '').strip()
                        if client_name:
                            client_names.add(client_name)
                            
                            # Check if client folder with images exists
                            client_folder = self._find_client_folder(client_name)
                            if not client_folder:
                                errors.append(
                                    f"⚠️ clients.csv, row {row_num}: No logo found for client '{client_name}' "
                                    f"(expected file: clients/{client_name}.jpg/png)"
                                )
                        else:
                            errors.append(f"❌ clients.csv, row {row_num}: client_name is empty")
            except Exception as e:
                errors.append(f"❌ Error validating clients.csv: {str(e)}")
        
        # Validate projects and check for project folders
        projects_csv_path = self._find_file('projects.csv')
        if projects_csv_path:
            try:
                with open(projects_csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row_num, row in enumerate(reader, start=2):
                        project_name = row.get('project_name', '').strip()
                        if not project_name:
                            errors.append(f"❌ projects.csv, row {row_num}: project_name is empty")
                            continue
                        
                        # Validate client reference
                        client_name = row.get('client_name', '').strip()
                        if client_name and client_name not in client_names:
                            errors.append(
                                f"❌ projects.csv, row {row_num}: Client '{client_name}' not found in clients.csv"
                            )
                        
                        # Validate year
                        year = row.get('year', '').strip()
                        if year:
                            try:
                                year_int = int(year)
                                if year_int < 1900 or year_int > 2100:
                                    errors.append(
                                        f"❌ projects.csv, row {row_num}: Year '{year}' is out of valid range (1900-2100)"
                                    )
                            except ValueError:
                                errors.append(f"❌ projects.csv, row {row_num}: Year '{year}' is not a valid number")
                        else:
                            errors.append(f"❌ projects.csv, row {row_num}: year is empty")
                        
                        # Validate expertise codes
                        expertise_str = row.get('expertise', '').strip()
                        if expertise_str:
                            valid_codes = {'SS', 'TMS', 'RF', 'CD', 'SC'}
                            expertise_codes = [e.strip() for e in expertise_str.split(',') if e.strip()]
                            invalid_codes = [code for code in expertise_codes if code not in valid_codes]
                            if invalid_codes:
                                errors.append(
                                    f"❌ projects.csv, row {row_num}: Invalid expertise codes: {', '.join(invalid_codes)}. "
                                    f"Valid codes are: SS, TMS, RF, CD, SC"
                                )
                        
                        # Check if project folder with images exists
                        project_folder = self._find_project_folder(project_name)
                        if not project_folder:
                            errors.append(
                                f"⚠️ projects.csv, row {row_num}: No images found for project '{project_name}' "
                                f"(expected in projects/{project_name}/ folder)"
                            )
            except Exception as e:
                errors.append(f"❌ Error validating projects.csv: {str(e)}")
        
        return errors
    
    def _extract_zip(self) -> str:
        """Extract zip file to temporary directory"""
        from django.core.files.uploadedfile import InMemoryUploadedFile
        
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_import')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file
        zip_path = os.path.join(temp_dir, 'upload.zip')
        with open(zip_path, 'wb+') as destination:
            for chunk in self.zip_file.chunks():
                destination.write(chunk)
        
        # Extract zip
        extract_dir = os.path.join(temp_dir, 'extracted')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        return extract_dir
    
    def _import_clients(self):
        """Import clients from clients.csv and auto-discover logos from folders"""
        from projects.models import Client
        
        csv_path = self._find_file('clients.csv')
        if not csv_path:
            self.errors.append("clients.csv not found in zip file")
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        client_name = row.get('client_name', '').strip()
                        if not client_name:
                            self.errors.append(f"Row {row_num}: client_name is required")
                            continue
                        
                        # Find logo image automatically from client folder
                        logo_path = self._find_first_image_in_client_folder(client_name)
                        
                        if not logo_path:
                            self.errors.append(
                                f"Row {row_num}: No logo image found for client '{client_name}' "
                                f"(expected file: clients/{client_name}.jpg/png in zip)"
                            )
                            continue
                        
                        # Check if client exists
                        client, created = Client.objects.get_or_create(
                            client_name=client_name,
                            defaults={
                                'client_website': row.get('client_website', '').strip(),
                            }
                        )
                        
                        # Update logo
                        with open(logo_path, 'rb') as img_file:
                            client.client_logo.save(
                                os.path.basename(logo_path),
                                File(img_file),
                                save=False
                            )
                        
                        # Update website if provided and different
                        website = row.get('client_website', '').strip()
                        if website and client.client_website != website:
                            client.client_website = website
                        
                        client.save()
                        
                        if created:
                            self.stats['clients_created'] += 1
                        else:
                            self.stats['clients_updated'] += 1
                            
                    except Exception as e:
                        self.errors.append(f"Row {row_num} in clients.csv: {str(e)}")
                        
        except Exception as e:
            self.errors.append(f"Error reading clients.csv: {str(e)}")
    
    def _import_projects(self):
        """Import projects from projects.csv"""
        from projects.models import Project, Client
        
        csv_path = self._find_file('projects.csv')
        if not csv_path:
            self.errors.append("projects.csv not found in zip file")
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):
                    try:
                        project_name = row.get('project_name', '').strip()
                        if not project_name:
                            self.errors.append(f"Row {row_num}: project_name is required")
                            continue
                        
                        # Get client
                        client_name = row.get('client_name', '').strip()
                        client = None
                        if client_name:
                            try:
                                client = Client.objects.get(client_name=client_name)
                            except Client.DoesNotExist:
                                self.errors.append(
                                    f"Row {row_num}: Client '{client_name}' not found for project '{project_name}'"
                                )
                                continue
                        
                        # Parse expertise (comma-separated values)
                        expertise_str = row.get('expertise', '').strip()
                        expertise = [e.strip() for e in expertise_str.split(',') if e.strip()]
                        
                        # Get or create project
                        project, created = Project.objects.update_or_create(
                            project_name=project_name,
                            defaults={
                                'client': client,
                                'city': row.get('city', '').strip(),
                                'project_description': row.get('project_description', '').strip(),
                                'architect': row.get('architect', '').strip(),
                                'expertise': expertise if expertise else [],
                                'year': int(row.get('year', 0)),
                            }
                        )
                        
                        if created:
                            self.stats['projects_created'] += 1
                        else:
                            self.stats['projects_updated'] += 1
                            
                    except ValueError as e:
                        self.errors.append(f"Row {row_num} in projects.csv: Invalid year value")
                    except Exception as e:
                        self.errors.append(f"Row {row_num} in projects.csv: {str(e)}")
                        
        except Exception as e:
            self.errors.append(f"Error reading projects.csv: {str(e)}")
    
    def _import_gallery_images_from_folders(self):
        """Import gallery images automatically from project folders"""
        from projects.models import GalleryImage, Project
        
        # Get all projects
        projects = Project.objects.all()
        
        for project in projects:
            try:
                # Find all images in project folder
                image_paths = self._find_all_images_in_project_folder(project.project_name)
                
                if not image_paths:
                    continue  # No images for this project
                
                for image_path in image_paths:
                    try:
                        image_filename = os.path.basename(image_path)
                        
                        # Create or get gallery image (avoid duplicates by checking image name)
                        gallery_image, created = GalleryImage.objects.get_or_create(
                            project=project,
                            image_description=image_filename.rsplit('.', 1)[0],  # Use filename without extension as description
                            defaults={}
                        )
                        
                        # Update image
                        with open(image_path, 'rb') as img_file:
                            gallery_image.image.save(
                                image_filename,
                                File(img_file),
                                save=True
                            )
                        
                        if created:
                            self.stats['gallery_images_created'] += 1
                        else:
                            self.stats['gallery_images_updated'] += 1
                            
                    except Exception as e:
                        self.errors.append(f"Error importing image '{image_filename}' for project '{project.project_name}': {str(e)}")
                        
            except Exception as e:
                self.errors.append(f"Error processing images for project '{project.project_name}': {str(e)}")
    
    def _update_project_cover_images(self):
        """Update cover images for projects - use first image in gallery"""
        from projects.models import Project, GalleryImage
        
        projects = Project.objects.all()
        
        for project in projects:
            try:
                # Get first gallery image for this project (alphabetically)
                first_image = GalleryImage.objects.filter(project=project).order_by('id').first()
                
                if first_image and not project.cover_image:
                    project.cover_image = first_image
                    project.save()
                    
            except Exception as e:
                # Non-critical errors
                pass
    
    def _find_file(self, filename: str) -> str:
        """Find a file in the extracted directory"""
        for root, dirs, files in os.walk(self.temp_dir):
            if filename in files:
                return os.path.join(root, filename)
        return None
    
    def _find_client_folder(self, client_name: str) -> str:
        """Find client logo file (named ClientName.ext in clients/ folder)"""
        # Look for files named like "ClientName.jpg" directly in clients/ folder
        clients_dir = os.path.join(self.temp_dir, 'clients')
        if os.path.exists(clients_dir) and os.path.isdir(clients_dir):
            for file in os.listdir(clients_dir):
                # Check if file matches client name (without extension)
                file_name_without_ext = os.path.splitext(file)[0]
                if file_name_without_ext == client_name and file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    return clients_dir
        return None
    
    def _find_project_folder(self, project_name: str) -> str:
        """Find folder containing project images"""
        search_patterns = [
            os.path.join(self.temp_dir, 'projects', project_name),
            os.path.join(self.temp_dir, project_name),
        ]
        
        for pattern in search_patterns:
            if os.path.exists(pattern) and os.path.isdir(pattern):
                # Check if folder has images
                for root, dirs, files in os.walk(pattern):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            return pattern
        return None
    
    def _find_first_image_in_client_folder(self, client_name: str) -> str:
        """Find client logo file named ClientName.ext in clients/ folder"""
        clients_dir = os.path.join(self.temp_dir, 'clients')
        if not os.path.exists(clients_dir):
            return None
        
        # Look for file matching client name
        for file in os.listdir(clients_dir):
            file_name_without_ext = os.path.splitext(file)[0]
            if file_name_without_ext == client_name and file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return os.path.join(clients_dir, file)
        
        return None
    
    def _find_all_images_in_project_folder(self, project_name: str) -> List[str]:
        """Find all images in project folder"""
        folder = self._find_project_folder(project_name)
        if not folder:
            return []
        
        image_paths = []
        for root, dirs, files in os.walk(folder):
            for file in sorted(files):  # Sort for consistency
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_paths.append(os.path.join(root, file))
        return image_paths
    
    def _find_image_in_folders(self, filename: str, folder_path: List[str]) -> str:
        """
        Find an image file in the extracted directory
        Searches in multiple potential locations
        """
        if not filename:
            return None
        
        # Search patterns
        search_paths = [
            # Direct path
            os.path.join(self.temp_dir, *folder_path, filename),
            # Without first folder level
            os.path.join(self.temp_dir, *folder_path[1:], filename) if len(folder_path) > 1 else None,
            # Just the last folder
            os.path.join(self.temp_dir, folder_path[-1], filename) if folder_path else None,
            # Root level
            os.path.join(self.temp_dir, filename),
        ]
        
        # Check each path
        for path in search_paths:
            if path and os.path.exists(path):
                return path
        
        # Recursive search as fallback
        for root, dirs, files in os.walk(self.temp_dir):
            if filename in files:
                return os.path.join(root, filename)
        
        return None
