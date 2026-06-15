import os
import logging
import json
from typing import List, Dict
from pathlib import Path
import requests
from datetime import datetime

logger = logging.getLogger(__name__)


class DataManager:
    """Manage medical PDF data - download, organize, validate."""

    def __init__(self, data_dir: str = "data/medical_pdfs"):
        self.data_dir = data_dir
        self.catalog_file = os.path.join(data_dir, "catalog.json")
        Path(data_dir).mkdir(parents=True, exist_ok=True)

    def download_pdf(self, url: str, filename: str) -> bool:
        """
        Download a PDF from URL.

        Args:
            url: URL of the PDF
            filename: Name to save as

        Returns:
            Success status
        """
        filepath = os.path.join(self.data_dir, filename)

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            logger.info(f"Downloaded: {filename} ({len(response.content)} bytes)")
            return True
        except Exception as e:
            logger.error(f"Error downloading {filename}: {str(e)}")
            return False

    def get_pdf_files(self) -> List[str]:
        """Get all PDF files in data directory."""
        pdfs = [f for f in os.listdir(self.data_dir) if f.endswith(".pdf")]
        return sorted(pdfs)

    def get_data_statistics(self) -> Dict:
        """Get statistics about the data directory."""
        pdfs = self.get_pdf_files()
        total_size = 0
        file_stats = []

        for pdf in pdfs:
            filepath = os.path.join(self.data_dir, pdf)
            size = os.path.getsize(filepath)
            total_size += size
            file_stats.append({
                "filename": pdf,
                "size_bytes": size,
                "size_mb": round(size / (1024 * 1024), 2)
            })

        return {
            "total_files": len(pdfs),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "files": file_stats,
            "timestamp": datetime.now().isoformat()
        }

    def save_catalog(self, metadata: Dict) -> bool:
        """Save data catalog to JSON file."""
        try:
            with open(self.catalog_file, "w") as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Catalog saved to {self.catalog_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving catalog: {str(e)}")
            return False

    def load_catalog(self) -> Dict:
        """Load data catalog from JSON file."""
        if os.path.exists(self.catalog_file):
            try:
                with open(self.catalog_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading catalog: {str(e)}")
        return {}

    def display_statistics(self) -> None:
        """Display data statistics in a formatted way."""
        stats = self.get_data_statistics()

        print("\n" + "=" * 60)
        print("📊 DATA STATISTICS")
        print("=" * 60)
        print(f"Total PDF Files: {stats['total_files']}")
        print(f"Total Size: {stats['total_size_mb']} MB")
        print(f"\n📄 Files in data/medical_pdfs/:")
        print("-" * 60)

        if stats['files']:
            for file in stats['files']:
                print(f"  • {file['filename']:<40} {file['size_mb']:>8} MB")
        else:
            print("  (No PDF files yet)")

        print("=" * 60 + "\n")

    def validate_pdfs(self) -> Dict:
        """Validate PDF files and check for issues."""
        try:
            from src.pdf_scraper import PDFScraper
        except ImportError:
            logger.warning("PDFScraper not available, skipping validation")
            return {
                "total_checked": 0,
                "valid": [],
                "invalid": [],
                "total_text_extracted": 0
            }

        pdfs = self.get_pdf_files()
        scraper = PDFScraper()
        validation_results = {
            "total_checked": len(pdfs),
            "valid": [],
            "invalid": [],
            "total_text_extracted": 0
        }

        for pdf in pdfs:
            filepath = os.path.join(self.data_dir, pdf)
            try:
                text = scraper.extract_text_from_pdf(filepath)
                if text and len(text) > 100:
                    validation_results["valid"].append({
                        "filename": pdf,
                        "text_length": len(text),
                        "status": "✅ Valid"
                    })
                    validation_results["total_text_extracted"] += len(text)
                else:
                    validation_results["invalid"].append({
                        "filename": pdf,
                        "reason": "Insufficient text extracted",
                        "status": "⚠️ Invalid"
                    })
            except Exception as e:
                validation_results["invalid"].append({
                    "filename": pdf,
                    "reason": str(e),
                    "status": "❌ Error"
                })

        return validation_results

    def display_validation_results(self, results: Dict) -> None:
        """Display validation results."""
        print("\n" + "=" * 60)
        print("✅ PDF VALIDATION RESULTS")
        print("=" * 60)
        print(f"Total Checked: {results['total_checked']}")
        print(f"Valid PDFs: {len(results['valid'])}")
        print(f"Invalid PDFs: {len(results['invalid'])}")
        print(f"Total Text Extracted: {results['total_text_extracted']:,} characters")

        if results['valid']:
            print("\n✅ Valid Files:")
            for file in results['valid']:
                print(f"  • {file['filename']:<40} ({file['text_length']:>8,} chars)")

        if results['invalid']:
            print("\n⚠️ Invalid/Error Files:")
            for file in results['invalid']:
                print(f"  • {file['filename']:<40} ({file['reason']})")

        print("=" * 60 + "\n")
