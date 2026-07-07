"""
Service for generating reports in various formats.
"""
import csv
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


class ReportService:
    """Service class for report generation."""
    
    @staticmethod
    def generate_csv_report(data, headers):
        """
        Generate CSV report from data.
        
        Args:
            data (list): List of dictionaries containing report data
            headers (list): List of column headers
            
        Returns:
            str: CSV content as string
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
        csv_content = output.getvalue()
        output.close()
        
        return csv_content
    
    @staticmethod
    def generate_inventory_csv():
        """Generate current inventory report as CSV."""
        from models.batch import Batch
        
        batches = Batch.query.all()
        
        data = []
        for batch in batches:
            data.append({
                'Batch ID': batch.batch_id,
                'Product Name': batch.product.product_name,
                'Category': batch.product.category,
                'Manufacturing Date': batch.manufacturing_date.strftime('%Y-%m-%d'),
                'Original Expiry': batch.original_expiry.strftime('%Y-%m-%d'),
                'Adjusted Expiry': batch.adjusted_expiry.strftime('%Y-%m-%d'),
                'Quantity': batch.quantity,
                'Status': batch.status,
                'Days Until Expiry': batch.days_until_expiry()
            })
        
        headers = ['Batch ID', 'Product Name', 'Category', 'Manufacturing Date', 
                  'Original Expiry', 'Adjusted Expiry', 'Quantity', 'Status', 'Days Until Expiry']
        
        return ReportService.generate_csv_report(data, headers)
    
    @staticmethod
    def generate_expiring_products_csv(days=7):
        """Generate expiring products report as CSV."""
        from models.batch import Batch
        
        batches = Batch.get_expiring_soon(days)
        
        data = []
        for batch in batches:
            data.append({
                'Batch ID': batch.batch_id,
                'Product Name': batch.product.product_name,
                'Category': batch.product.category,
                'Adjusted Expiry': batch.adjusted_expiry.strftime('%Y-%m-%d'),
                'Quantity': batch.quantity,
                'Status': batch.status,
                'Days Until Expiry': batch.days_until_expiry()
            })
        
        headers = ['Batch ID', 'Product Name', 'Category', 'Adjusted Expiry', 
                  'Quantity', 'Status', 'Days Until Expiry']
        
        return ReportService.generate_csv_report(data, headers)
    
    @staticmethod
    def generate_temperature_violations_csv(days=30):
        """Generate temperature violations report as CSV."""
        from models.temperature_log import TemperatureLog
        
        logs = TemperatureLog.get_recent_violations(days)
        
        data = []
        for log in logs:
            data.append({
                'Log ID': log.log_id,
                'Batch ID': log.batch_id,
                'Product Name': log.batch.product.product_name,
                'Temperature': f"{log.temperature}°C",
                'Max Safe Temp': f"{log.batch.product.maximum_temperature}°C",
                'Days Deducted': round(log.days_deducted, 2),
                'Recorded At': log.recorded_at.strftime('%Y-%m-%d %H:%M'),
                'Employee': log.employee_name
            })
        
        headers = ['Log ID', 'Batch ID', 'Product Name', 'Temperature', 'Max Safe Temp',
                  'Days Deducted', 'Recorded At', 'Employee']
        
        return ReportService.generate_csv_report(data, headers)
    
    @staticmethod
    def generate_pdf_report(title, data, headers):
        """
        Generate PDF report from data.
        
        Args:
            title (str): Report title
            data (list): List of lists containing table data
            headers (list): List of column headers
            
        Returns:
            bytes: PDF content as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        
        # Title
        title_para = Paragraph(title, title_style)
        elements.append(title_para)
        elements.append(Spacer(1, 0.25 * inch))
        
        # Date
        date_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        date_para = Paragraph(date_text, styles['Normal'])
        elements.append(date_para)
        elements.append(Spacer(1, 0.25 * inch))
        
        # Table
        table_data = [headers] + data
        table = Table(table_data)
        
        # Table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
