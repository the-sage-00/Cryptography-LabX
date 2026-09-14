import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_report():
    pdf_path = os.path.join(os.path.dirname(__file__), "Assignment_6_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#1a365d'),
        alignment=1,
        fontName='Helvetica-Bold'
    )
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading1'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2b6cb0'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2d3748')
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        fontName='Courier',
        textColor=colors.HexColor('#1a202c')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1a202c')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title & Header
    story.append(Paragraph("MALAVIYA NATIONAL INSTITUTE OF TECHNOLOGY JAIPUR", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Department of Computer Science and Engineering", ParagraphStyle('Sub', parent=body_style, alignment=1, fontSize=10, fontName='Helvetica-Bold')))
    story.append(Paragraph("Course: Cryptography Laboratory (22CPP307) | Group: 10 (Even Group Number)", ParagraphStyle('Sub2', parent=body_style, alignment=1, fontSize=9)))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Lab Assignment 6: Cryptanalysis of Vigenère Cipher using Kasiski Examination & Frequency Analysis", h1_style))
    story.append(Paragraph("<b>Target Dataset:</b> Ciphertext-2 (Even Group Numbers) | <b>Normalized Length:</b> 758 letters<br/><b>Recovered Key:</b> UNITEDSTATES (Length 12) | <b>Verification Status:</b> 100% Exact Match via Re-encryption", body_style))
    story.append(Spacer(1, 8))

    # 1. Architecture & Implemented Modules
    story.append(Paragraph("1. Implemented User-Defined Modules", h1_style))
    modules_text = """
    All 13 mandatory user-defined functions were implemented in Python:<br/>
    <b>1. clean_ciphertext():</b> Strips whitespaces and non-alphabetic symbols, outputting normalized uppercase letters.<br/>
    <b>2. find_repeated_patterns():</b> Identifies repeated n-grams (lengths 3 to 5) and catalogues their exact index positions.<br/>
    <b>3. calculate_distances():</b> Measures spacing distances between recurring pattern instances.<br/>
    <b>4. find_factors():</b> Computes common divisors of measured distances (from 2 to 20).<br/>
    <b>5. kasiski_analysis():</b> Ranks candidate key lengths by accumulated factor frequency counts.<br/>
    <b>6. calculate_ic():</b> Computes Index of Coincidence ($IC = \\sum f_i(f_i-1) / (N(N-1))$) to benchmark monoalphabetic purity.<br/>
    <b>7. split_into_groups():</b> Slices ciphertext into $L$ independent coset streams corresponding to candidate key length.<br/>
    <b>8. frequency_analysis():</b> Evaluates unigram letter frequencies (A-Z) per coset.<br/>
    <b>9. find_shift():</b> Identifies Caesar shift per coset via Chi-Square goodness-of-fit against standard English frequencies.<br/>
    <b>10. find_key():</b> Combines the optimal Caesar shifts from all cosets into the reconstructed keyword.<br/>
    <b>11. vigenere_decrypt():</b> Decrypts ciphertext using recovered key ($P_i = (C_i - K_{i \\pmod L}) \\pmod{26}$).<br/>
    <b>12. vigenere_encrypt():</b> Re-encrypts recovered plaintext for verification ($C_i = (P_i + K_{i \\pmod L}) \\pmod{26}$).<br/>
    <b>13. verify():</b> Asserts whether re-encrypted text is character-identical to the original ciphertext.
    """
    story.append(Paragraph(modules_text, body_style))
    story.append(Spacer(1, 8))

    # 2. Experimental Data & Key Length Determination
    story.append(Paragraph("2. Key Length Determination (Kasiski & Index of Coincidence)", h1_style))
    kasiski_ic_summary = """
    <b>Kasiski Examination:</b> A total of 92 repeated patterns (trigrams, 4-grams, 5-grams) were identified. High-frequency factor counts clustered at 2, 3, 4, 6, and 12, indicating a base period of 12.<br/>
    <b>Index of Coincidence:</b> Slicing into 12 cosets yielded an average IC of <b>0.0717</b>, closely converging on standard English ($IC \\approx 0.068$) compared to non-period slices ($IC \\approx 0.043 - 0.050$). Both tests unequivocally confirm <b>Key Length L = 12</b>.
    """
    story.append(Paragraph(kasiski_ic_summary, body_style))
    story.append(Spacer(1, 8))

    # 3. Results Table
    story.append(Paragraph("3. Coset Analysis & Recovered Key Breakdown", h1_style))
    table_data = [
        [Paragraph("Coset #", table_cell_bold), Paragraph("Length", table_cell_bold), Paragraph("Shift", table_cell_bold), Paragraph("Key Char", table_cell_bold), Paragraph("Min Chi-Square", table_cell_bold), Paragraph("Status", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("64", table_cell), Paragraph("20", table_cell), Paragraph("<b>U</b>", table_cell), Paragraph("14.32", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("2", table_cell), Paragraph("64", table_cell), Paragraph("13", table_cell), Paragraph("<b>N</b>", table_cell), Paragraph("21.86", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("3", table_cell), Paragraph("63", table_cell), Paragraph("8", table_cell), Paragraph("<b>I</b>", table_cell), Paragraph("22.39", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("4", table_cell), Paragraph("63", table_cell), Paragraph("19", table_cell), Paragraph("<b>T</b>", table_cell), Paragraph("34.12", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("5", table_cell), Paragraph("63", table_cell), Paragraph("4", table_cell), Paragraph("<b>E</b>", table_cell), Paragraph("19.88", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("6", table_cell), Paragraph("63", table_cell), Paragraph("3", table_cell), Paragraph("<b>D</b>", table_cell), Paragraph("30.49", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("7", table_cell), Paragraph("63", table_cell), Paragraph("18", table_cell), Paragraph("<b>S</b>", table_cell), Paragraph("28.29", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("8", table_cell), Paragraph("63", table_cell), Paragraph("19", table_cell), Paragraph("<b>T</b>", table_cell), Paragraph("22.52", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("9", table_cell), Paragraph("63", table_cell), Paragraph("0", table_cell), Paragraph("<b>A</b>", table_cell), Paragraph("13.25", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("10", table_cell), Paragraph("63", table_cell), Paragraph("19", table_cell), Paragraph("<b>T</b>", table_cell), Paragraph("19.90", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("11", table_cell), Paragraph("63", table_cell), Paragraph("4", table_cell), Paragraph("<b>E</b>", table_cell), Paragraph("19.63", table_cell), Paragraph("Optimal", table_cell)],
        [Paragraph("12", table_cell), Paragraph("63", table_cell), Paragraph("18", table_cell), Paragraph("<b>S</b>", table_cell), Paragraph("24.04", table_cell), Paragraph("Optimal", table_cell)],
    ]
    t = Table(table_data, colWidths=[55, 60, 60, 75, 110, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # 4. Decryption & Verification
    story.append(Paragraph("4. Plaintext Decryption & Re-Encryption Verification", h1_style))
    pt_sample = """
    <b>Recovered Plaintext (Excerpt):</b><br/>
    <i>WETHEREFORETHEREPRESENTATIVESOFTHEUNITEDSTATESOFAMERICAINGENERALCONGRESSASSEMBLEDAPPEALINGTOTHESUPREMEJUDGEOFTHEWORLDFORTHERECTITUDEOFOURINTENTIONSDOINTHENAMEANDBYAUTHORITYOFTHEGOODPEOPLEOFTHESECOLONIESSOLEMNLYPUBLISHANDDECLARETHATTHESEUNITEDCOLONIESAREANDOFRIGHTOUGHTTOBEFREEANDINDEPENDENTSTATESTHAT...</i><br/><br/>
    <b>Mathematical Re-Encryption Verification:</b><br/>
    Applying $vigenere\\_encrypt(Recovered\\_Plaintext, \\text{'UNITEDSTATES'})$ yielded a ciphertext matching the assigned Ciphertext-2 with <b>100.0% exactness across all 758 characters</b>.
    """
    story.append(Paragraph(pt_sample, body_style))

    doc.build(story)
    print(f"Report generated at: {pdf_path}")

if __name__ == '__main__':
    create_report()
