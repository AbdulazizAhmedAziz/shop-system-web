#!/usr/bin/env python3
"""
Generate PDF from SRS Document
Creates a professional PDF document from the SRS markdown content
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import re

# Custom colors
PRIMARY_BLUE = HexColor('#0066CC')
SECONDARY_BLUE = HexColor('#3399FF')
ACCENT_ORANGE = HexColor('#FF8C00')
LIGHT_GRAY = HexColor('#F5F5F5')
DARK_GRAY = HexColor('#404040')

class NumberedCanvas(canvas.Canvas):
    """Canvas with page numbers and headers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(DARK_GRAY)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 0.75*inch, 0.75*inch, page_text)
        self.drawString(0.75*inch, 0.75*inch, "Smart Shop System - SRS Document v1.0")
        self.restoreState()

def create_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()
    
    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY_BLUE,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Chapter style
    styles.add(ParagraphStyle(
        name='Chapter',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=PRIMARY_BLUE,
        spaceAfter=12,
        spaceBefore=24,
        fontName='Helvetica-Bold'
    ))
    
    # Section style
    styles.add(ParagraphStyle(
        name='Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=PRIMARY_BLUE,
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    ))
    
    # Subsection style
    styles.add(ParagraphStyle(
        name='Subsection',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=SECONDARY_BLUE,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    # Info box style
    styles.add(ParagraphStyle(
        name='InfoBox',
        parent=styles['Normal'],
        fontSize=10,
        backColor=LIGHT_GRAY,
        borderColor=PRIMARY_BLUE,
        borderWidth=1,
        borderPadding=10,
        leftIndent=10,
        rightIndent=10,
        spaceAfter=10
    ))
    
    # Code style
    if 'Code' not in styles.byName:
        styles.add(ParagraphStyle(
            name='Code',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Courier',
            textColor=DARK_GRAY,
            leftIndent=20,
            rightIndent=20,
            backColor=LIGHT_GRAY,
            borderPadding=5
        ))
    
    return styles

def parse_markdown(text):
    """Simple markdown parser for basic formatting"""
    # Headers
    text = re.sub(r'^# (.+)$', r'<b><font color="#0066CC" size="18">\1</font></b>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<b><font color="#0066CC" size="14">\1</font></b>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<b><font color="#3399FF" size="12">\1</font></b>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    
    # Code
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="9" color="#404040">\1</font>', text)
    
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<link href="\2" color="#0066CC"><u>\1</u></link>', text)
    
    # Lists
    text = re.sub(r'^- (.+)$', r'• \1', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\. (.+)$', r'\1', text, flags=re.MULTILINE)
    
    return text

def create_title_page(canvas_obj, doc):
    """Create title page"""
    if canvas_obj._pageNumber == 1:
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica-Bold", 28)
        canvas_obj.setFillColor(PRIMARY_BLUE)
        
        # Title
        title = "Software Requirements\nSpecification (SRS)"
        canvas_obj.drawCentredString(A4[0]/2, A4[1] - 2*inch, title)
        
        # Subtitle
        canvas_obj.setFont("Helvetica-Bold", 20)
        canvas_obj.setFillColor(DARK_GRAY)
        canvas_obj.drawCentredString(A4[0]/2, A4[1] - 3*inch, "Smart Shop System")
        
        # Description
        canvas_obj.setFont("Helvetica", 14)
        canvas_obj.drawCentredString(A4[0]/2, A4[1] - 3.5*inch, "E-Commerce Web Application")
        
        # Document info box
        info_y = A4[1] - 5*inch
        canvas_obj.setFillColor(LIGHT_GRAY)
        canvas_obj.rect(1*inch, info_y - 1.5*inch, A4[0] - 2*inch, 1.5*inch, fill=1)
        canvas_obj.setFillColor(PRIMARY_BLUE)
        canvas_obj.rect(1*inch, info_y - 1.5*inch, A4[0] - 2*inch, 2, fill=1)
        
        canvas_obj.setFillColor(DARK_GRAY)
        canvas_obj.setFont("Helvetica", 11)
        info_text = [
            "Version: 1.0",
            "Date: December 11, 2025",
            "Author: Development Team",
            "Status: Approved",
            "Classification: Internal Use"
        ]
        y_pos = info_y - 0.3*inch
        for line in info_text:
            canvas_obj.drawString(1.2*inch, y_pos, line)
            y_pos -= 0.25*inch
        
        # Footer
        canvas_obj.setFont("Helvetica-Oblique", 10)
        canvas_obj.drawCentredString(A4[0]/2, 1.5*inch, 
            "This document specifies the requirements for the Smart Shop System,")
        canvas_obj.drawCentredString(A4[0]/2, 1.3*inch, 
            "a web-based e-commerce platform.")
        
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawCentredString(A4[0]/2, 0.5*inch, "Confidential - For Internal Use Only")
        
        canvas_obj.restoreState()
    else:
        # Regular pages - just page numbers
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(DARK_GRAY)
        page_text = f"Page {canvas_obj._pageNumber}"
        canvas_obj.drawRightString(A4[0] - 0.75*inch, 0.75*inch, page_text)
        canvas_obj.drawString(0.75*inch, 0.75*inch, "Smart Shop System - SRS Document v1.0")
        canvas_obj.restoreState()

def generate_pdf():
    """Generate PDF from SRS content"""
    filename = "SRS_Document.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = create_styles()
    story = []
    
    # Title Page - will be handled by onFirstPage callback
    story.append(PageBreak())
    
    # Table of Contents placeholder
    story.append(PageBreak())
    story.append(Paragraph("Table of Contents", styles['Chapter']))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Introduction",
        "2. Overall Description",
        "3. System Features",
        "4. External Interface Requirements",
        "5. System Architecture",
        "6. Non-Functional Requirements",
        "7. User Stories",
        "8. Use Cases",
        "9. Data Model",
        "10. Security Requirements",
        "11. Performance Requirements",
        "12. Testing Requirements",
        "13. Deployment Requirements",
        "14. Appendices"
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # Chapter 1: Introduction
    story.append(Paragraph("1. Introduction", styles['Chapter']))
    
    story.append(Paragraph("1.1 Purpose", styles['Section']))
    story.append(Paragraph(
        "This document specifies the requirements for the Smart Shop System, a web-based "
        "e-commerce platform that enables online shopping with advanced features including "
        "product management, shopping cart functionality, order processing, and promotional offers.",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1.2 Scope", styles['Section']))
    story.append(Paragraph("The Smart Shop System is designed to:", styles['Normal']))
    scope_items = [
        "Provide a user-friendly web interface for customers to browse and purchase products",
        "Enable administrators to manage inventory, products, and promotional offers",
        "Support multiple user roles (Admin and Customer)",
        "Handle order processing and payment methods",
        "Implement promotional offers with discounts, gifts, and purchase limits"
    ]
    for item in scope_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1.3 Definitions, Acronyms, and Abbreviations", styles['Section']))
    definitions = [
        ("SRS", "Software Requirements Specification"),
        ("UI", "User Interface"),
        ("API", "Application Programming Interface"),
        ("Admin", "Administrator user role"),
        ("Customer", "Regular user role"),
        ("COD", "Cash on Delivery"),
        ("POS", "Point of Sale (Visa on Delivery)"),
        ("MVC", "Model-View-Controller"),
        ("WSGI", "Web Server Gateway Interface"),
        ("RTL", "Right-to-Left (text direction)")
    ]
    for term, definition in definitions:
        story.append(Paragraph(f"<b>{term}:</b> {definition}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1.4 References", styles['Section']))
    references = [
        "Flask Framework Documentation: https://flask.palletsprojects.com/",
        "Python 3.11 Documentation: https://docs.python.org/3.11/",
        "Railway Deployment Guide: https://docs.railway.app/"
    ]
    for ref in references:
        story.append(Paragraph(f"• {ref}", styles['Normal']))
    story.append(PageBreak())
    
    # Chapter 2: Overall Description
    story.append(Paragraph("2. Overall Description", styles['Chapter']))
    
    story.append(Paragraph("2.1 Product Perspective", styles['Section']))
    story.append(Paragraph("The Smart Shop System is a standalone web application built using:", styles['Normal']))
    tech_stack = [
        "<b>Backend:</b> Python 3.11 with Flask framework",
        "<b>Frontend:</b> HTML, CSS, JavaScript",
        "<b>Deployment:</b> Railway cloud platform",
        "<b>Architecture:</b> Model-View-Controller (MVC) pattern"
    ]
    for item in tech_stack:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.2 Product Functions", styles['Section']))
    story.append(Paragraph("The system provides the following main functions:", styles['Normal']))
    functions = [
        "User authentication and authorization",
        "Product catalog management",
        "Shopping cart functionality",
        "Order processing",
        "Promotional offer management",
        "Inventory management",
        "Sales reporting"
    ]
    for i, func in enumerate(functions, 1):
        story.append(Paragraph(f"{i}. {func}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2.3 User Classes and Characteristics", styles['Section']))
    
    story.append(Paragraph("2.3.1 Administrator", styles['Subsection']))
    admin_info = [
        "<b>Responsibilities:</b> Manage products, inventory, offers, and view sales",
        "<b>Access Level:</b> Full system access",
        "<b>Default Credentials:</b> admin/123 or place/123"
    ]
    for info in admin_info:
        story.append(Paragraph(f"• {info}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("2.3.2 Customer", styles['Subsection']))
    customer_info = [
        "<b>Responsibilities:</b> Browse products, add to cart, place orders",
        "<b>Access Level:</b> Limited to shopping features",
        "<b>Registration:</b> Can create new account"
    ]
    for info in customer_info:
        story.append(Paragraph(f"• {info}", styles['Normal']))
    story.append(PageBreak())
    
    # Chapter 3: System Features
    story.append(Paragraph("3. System Features", styles['Chapter']))
    
    story.append(Paragraph("3.1 User Authentication", styles['Section']))
    
    story.append(Paragraph("3.1.1 Login", styles['Subsection']))
    story.append(Paragraph("<b>Priority:</b> High", styles['Normal']))
    story.append(Paragraph("<b>Description:</b> Users can log in with username and password", styles['Normal']))
    story.append(Paragraph("<b>Input:</b> Username, Password", styles['Normal']))
    story.append(Paragraph("<b>Output:</b> Redirect to appropriate dashboard", styles['Normal']))
    story.append(Paragraph("<b>Validation:</b>", styles['Normal']))
    story.append(Paragraph("• Username and password must match existing account", styles['Normal']))
    story.append(Paragraph("• Case-sensitive username", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("3.1.2 Registration", styles['Subsection']))
    story.append(Paragraph("<b>Priority:</b> High", styles['Normal']))
    story.append(Paragraph("<b>Description:</b> New customers can create accounts", styles['Normal']))
    story.append(Paragraph("<b>Input:</b> Username, Password", styles['Normal']))
    story.append(Paragraph("<b>Output:</b> New user account created, auto-login", styles['Normal']))
    story.append(Paragraph("<b>Validation:</b>", styles['Normal']))
    story.append(Paragraph("• Username must be unique", styles['Normal']))
    story.append(Paragraph("• Username cannot be empty", styles['Normal']))
    story.append(Paragraph("• Password cannot be empty", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("3.2 Product Management (Admin)", styles['Section']))
    
    story.append(Paragraph("3.2.1 View Products", styles['Subsection']))
    story.append(Paragraph("<b>Priority:</b> High", styles['Normal']))
    story.append(Paragraph("<b>Description:</b> Admin can view all products with details", styles['Normal']))
    story.append(Paragraph("<b>Display:</b> Table format with ID, Name, Price, Stock, Offers", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("3.2.2 Edit Product", styles['Subsection']))
    story.append(Paragraph("<b>Priority:</b> High", styles['Normal']))
    story.append(Paragraph("<b>Description:</b> Admin can modify product information", styles['Normal']))
    story.append(Paragraph("<b>Editable Fields:</b> Name, Price, Stock", styles['Normal']))
    story.append(Paragraph("<b>Validation:</b>", styles['Normal']))
    story.append(Paragraph("• Price must be positive number", styles['Normal']))
    story.append(Paragraph("• Stock must be non-negative integer", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("3.3 Shopping Cart", styles['Section']))
    
    story.append(Paragraph("3.3.1 Add to Cart", styles['Subsection']))
    story.append(Paragraph("<b>Priority:</b> High", styles['Normal']))
    story.append(Paragraph("<b>Description:</b> Customers can add products to shopping cart", styles['Normal']))
    story.append(Paragraph("<b>Input:</b> Product ID, Quantity", styles['Normal']))
    story.append(Paragraph("<b>Validation:</b>", styles['Normal']))
    story.append(Paragraph("• Quantity must be positive", styles['Normal']))
    story.append(Paragraph("• Quantity cannot exceed available stock", styles['Normal']))
    story.append(Paragraph("• If offer limit exists, total quantity in cart cannot exceed limit", styles['Normal']))
    story.append(Paragraph("<b>Output:</b> Product added to cart, cart count updated", styles['Normal']))
    story.append(PageBreak())
    
    # Chapter 4: Data Model
    story.append(Paragraph("4. Data Model", styles['Chapter']))
    
    story.append(Paragraph("4.1 Product Entity", styles['Section']))
    product_code = """Product {
    id: Integer (Primary Key)
    name: String
    price: Float
    stock: Integer
    category: String
    offer_discount: Float (0-100)
    offer_gift: String (nullable)
    offer_limit: Integer (0 = unlimited)
}"""
    story.append(Paragraph(product_code, styles['Code']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.2 User Entity", styles['Section']))
    user_code = """User {
    username: String (Primary Key)
    password: String
    role: String ("Admin" | "Customer")
    cart: Array<CartItem>
}

CartItem {
    product: Product
    qty: Integer
}"""
    story.append(Paragraph(user_code, styles['Code']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4.3 Order Entity", styles['Section']))
    order_code = """Order {
    order_id: Integer (Primary Key)
    customer_name: String
    items_txt: Array<String>
    total: Float
    address: String
    pay_method: String
    pay_status: String
    date: DateTime
}"""
    story.append(Paragraph(order_code, styles['Code']))
    story.append(PageBreak())
    
    # Chapter 5: Security Requirements
    story.append(Paragraph("5. Security Requirements", styles['Chapter']))
    
    story.append(Paragraph("5.1 Authentication", styles['Section']))
    auth_items = [
        "<b>Method:</b> Username/password",
        "<b>Session:</b> Flask session management",
        "<b>Timeout:</b> Session expires on browser close",
        "<b>Password Policy:</b> None (for MVP)"
    ]
    for item in auth_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("5.2 Authorization", styles['Section']))
    authz_items = [
        "<b>Role-based:</b> Admin vs Customer",
        "<b>Access Control:</b> Routes protected by role check",
        "<b>Default Admin:</b> admin/123, place/123"
    ]
    for item in authz_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(PageBreak())
    
    # Chapter 6: Performance Requirements
    story.append(Paragraph("6. Performance Requirements", styles['Chapter']))
    
    story.append(Paragraph("6.1 Response Times", styles['Section']))
    perf_items = [
        "<b>Page Load:</b> < 2 seconds",
        "<b>API Response:</b> < 500ms",
        "<b>Cart Update:</b> < 300ms",
        "<b>Checkout:</b> < 1 second"
    ]
    for item in perf_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("6.2 Throughput", styles['Section']))
    throughput_items = [
        "<b>Concurrent Users:</b> 50+ users",
        "<b>Requests per Second:</b> 100+ requests",
        "<b>Database Operations:</b> N/A (in-memory)"
    ]
    for item in throughput_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(PageBreak())
    
    # Chapter 7: Deployment Requirements
    story.append(Paragraph("7. Deployment Requirements", styles['Chapter']))
    
    story.append(Paragraph("7.1 Deployment Platform", styles['Section']))
    deploy_items = [
        "<b>Platform:</b> Railway",
        "<b>URL:</b> https://railway.app",
        "<b>Build:</b> Automatic from GitHub",
        "<b>Runtime:</b> Python 3.11"
    ]
    for item in deploy_items:
        story.append(Paragraph(f"• {item}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("7.2 Dependencies", styles['Section']))
    story.append(Paragraph("<b>Python:</b> 3.11+", styles['Normal']))
    story.append(Paragraph("<b>Packages:</b>", styles['Normal']))
    packages = [
        "Flask==3.0.0",
        "Werkzeug==3.0.1",
        "gunicorn==21.2.0"
    ]
    for pkg in packages:
        story.append(Paragraph(f"• {pkg}", styles['Normal']))
    story.append(PageBreak())
    
    # Appendices
    story.append(Paragraph("8. Appendices", styles['Chapter']))
    
    story.append(Paragraph("8.1 Glossary", styles['Section']))
    glossary = [
        ("MVP", "Minimum Viable Product"),
        ("RTL", "Right-to-Left (text direction)"),
        ("WSGI", "Web Server Gateway Interface"),
        ("COD", "Cash on Delivery"),
        ("POS", "Point of Sale")
    ]
    for term, definition in glossary:
        story.append(Paragraph(f"<b>{term}:</b> {definition}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("8.2 Future Enhancements", styles['Section']))
    enhancements = [
        "Database integration (PostgreSQL)",
        "User password hashing",
        "Email notifications",
        "Payment gateway integration",
        "Product images",
        "Search functionality",
        "Product reviews",
        "Wishlist feature",
        "Order tracking",
        "Admin analytics dashboard"
    ]
    for i, enhancement in enumerate(enhancements, 1):
        story.append(Paragraph(f"{i}. {enhancement}", styles['Normal']))
    
    # Build PDF with custom canvas
    class MyCanvas(NumberedCanvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._page_count = 0
        
        def showPage(self):
            if self._pageNumber == 1:
                create_title_page(self, doc)
            else:
                create_title_page(self, doc)
            super().showPage()
    
    doc.build(story, canvasmaker=MyCanvas)
    print(f"✅ PDF generated successfully: {filename}")

if __name__ == "__main__":
    try:
        generate_pdf()
    except ImportError:
        print("❌ Error: reportlab is not installed")
        print("Install it with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")

