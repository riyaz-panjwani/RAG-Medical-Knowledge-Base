#!/usr/bin/env python3
"""
Generate medical PDF files using reportlab for proper PDF creation.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY
from pathlib import Path

# Medical content for PDFs
MEDICAL_DOCUMENTS = [
    {
        "filename": "diabetes_overview.pdf",
        "title": "Diabetes Overview",
        "content": """<b>DIABETES OVERVIEW</b><br/><br/>
<b>What is Diabetes?</b><br/>
Diabetes is a chronic condition that affects how your body processes blood sugar (glucose). There are three main types of diabetes: Type 1, Type 2, and Gestational diabetes.<br/><br/>

<b>Type 1 Diabetes:</b><br/>
- Autoimmune condition where pancreas doesn't produce insulin<br/>
- Typically diagnosed in children and young adults<br/>
- Requires daily insulin injections or pump therapy<br/><br/>

<b>Type 2 Diabetes:</b><br/>
- Most common form (90-95% of cases)<br/>
- Body doesn't use insulin effectively (insulin resistance)<br/>
- Often associated with obesity and sedentary lifestyle<br/>
- Can often be managed with lifestyle changes and medication<br/><br/>

<b>Symptoms:</b><br/>
- Increased thirst<br/>
- Frequent urination<br/>
- Fatigue<br/>
- Blurred vision<br/>
- Slow healing of cuts or wounds<br/><br/>

<b>Risk Factors:</b><br/>
- Family history of diabetes<br/>
- Obesity<br/>
- Physical inactivity<br/>
- Poor diet high in sugar and processed foods<br/>
- Age over 45 years old<br/><br/>

<b>Management:</b><br/>
- Blood sugar monitoring<br/>
- Healthy diet and exercise<br/>
- Medication (if prescribed)<br/>
- Regular medical checkups<br/>
- Stress management<br/><br/>

<b>Complications:</b><br/>
- Heart disease and stroke<br/>
- Kidney disease<br/>
- Vision problems (diabetic retinopathy)<br/>
- Nerve damage (neuropathy)<br/>
- Foot problems<br/><br/>

<b>Prevention:</b><br/>
- Maintain healthy weight<br/>
- Exercise regularly (150 minutes per week)<br/>
- Eat healthy diet rich in vegetables<br/>
- Reduce sugar and processed food intake<br/>
- Get regular checkups"""
    },
    {
        "filename": "hypertension_management.pdf",
        "title": "Hypertension Management Guide",
        "content": """<b>HYPERTENSION MANAGEMENT GUIDE</b><br/><br/>
<b>What is High Blood Pressure?</b><br/>
Hypertension, or high blood pressure, is a common condition where the force of blood against artery walls is too high, usually 140/90 mmHg or higher.<br/><br/>

<b>Blood Pressure Categories:</b><br/>
- Normal: Less than 120/80 mmHg<br/>
- Elevated: Systolic 120-129 and Diastolic less than 80<br/>
- Stage 1 Hypertension: Systolic 130-139 or Diastolic 80-89<br/>
- Stage 2 Hypertension: Systolic 140 or higher or Diastolic 90 or higher<br/><br/>

<b>Causes:</b><br/>
Primary Hypertension (90-95% of cases):<br/>
- No identifiable secondary cause<br/>
- Often related to genetics, age, and lifestyle factors<br/><br/>

Secondary Hypertension:<br/>
- Kidney disease<br/>
- Thyroid problems<br/>
- Sleep apnea<br/>
- Certain medications<br/><br/>

<b>Risk Factors:</b><br/>
- Age (risk increases with age)<br/>
- Family history<br/>
- Obesity<br/>
- Excessive alcohol use<br/>
- High sodium diet<br/>
- Stress<br/>
- Physical inactivity<br/><br/>

<b>Treatment Options:</b><br/>
Lifestyle Changes:<br/>
- DASH diet (low sodium, high potassium)<br/>
- Regular aerobic exercise (150 minutes/week)<br/>
- Weight loss if overweight<br/>
- Limit alcohol<br/>
- Stress management<br/>
- Quit smoking<br/><br/>

<b>Medications:</b><br/>
- ACE inhibitors<br/>
- Beta-blockers<br/>
- Calcium channel blockers<br/>
- Diuretics<br/>
- ARBs (Angiotensin II receptor blockers)<br/><br/>

<b>Prevention:</b><br/>
- Check blood pressure regularly<br/>
- Keep a blood pressure log<br/>
- Home monitoring devices<br/>
- Regular doctor visits"""
    },
    {
        "filename": "heart_disease_prevention.pdf",
        "title": "Heart Disease Prevention",
        "content": """<b>HEART DISEASE PREVENTION</b><br/><br/>
<b>Heart Disease Facts:</b><br/>
Heart disease is the leading cause of death in the United States. Prevention is crucial and can significantly reduce risk.<br/><br/>

<b>Types of Heart Disease:</b><br/>
1. Coronary Artery Disease (CAD) - Most common type, plaque buildup in arteries<br/>
2. Heart Failure - Heart can't pump enough blood<br/>
3. Arrhythmias - Irregular heartbeat<br/>
4. Valvular Heart Disease - Problems with heart valves<br/><br/>

<b>Risk Factors You Cannot Change:</b><br/>
- Age<br/>
- Sex<br/>
- Family history<br/>
- Race/ethnicity<br/><br/>

<b>Risk Factors You Can Change:</b><br/>
- High blood pressure<br/>
- High cholesterol<br/>
- Smoking<br/>
- Obesity<br/>
- Physical inactivity<br/>
- Diabetes<br/>
- Stress<br/><br/>

<b>Prevention Strategies:</b><br/>
Nutrition:<br/>
- Mediterranean diet<br/>
- Limit saturated fats (less than 5% of calories)<br/>
- Eliminate trans fats<br/>
- Increase fiber (25-30g daily)<br/>
- Limit sodium to less than 2,300mg daily<br/><br/>

Exercise:<br/>
- 150 minutes of moderate aerobic activity per week<br/>
- Strength training 2 days per week<br/>
- Flexibility exercises<br/><br/>

<b>Screening:</b><br/>
- Cholesterol screening every 4-6 years<br/>
- Blood pressure monitoring<br/>
- Blood sugar screening<br/>
- EKG if symptoms present<br/><br/>

<b>Signs of Heart Attack:</b><br/>
- Chest pain or pressure<br/>
- Shortness of breath<br/>
- Pain in arm, neck, jaw<br/>
- Nausea or dizziness<br/><br/>
Action: Call 911 immediately if experiencing these symptoms"""
    },
    {
        "filename": "mental_health_wellbeing.pdf",
        "title": "Mental Health and Wellbeing",
        "content": """<b>MENTAL HEALTH AND WELLBEING</b><br/><br/>
<b>What is Mental Health?</b><br/>
Mental health includes emotional, psychological, and social wellbeing. It's as important as physical health.<br/><br/>

<b>Common Mental Health Conditions:</b><br/>
Depression: Persistent sadness and loss of interest, affects daily functioning, more than just being sad, treatable with therapy and/or medication<br/><br/>

Anxiety Disorders: Excessive worry and fear, physical symptoms like racing heart and sweating, can be generalized or specific<br/><br/>

<b>Risk Factors:</b><br/>
- Genetics/family history<br/>
- Brain chemistry<br/>
- Trauma or adverse events<br/>
- Chronic stress<br/>
- Substance abuse<br/>
- Medical conditions<br/>
- Social isolation<br/><br/>

<b>Support and Treatment:</b><br/>
Therapy Options:<br/>
- Cognitive Behavioral Therapy (CBT)<br/>
- Psychotherapy<br/>
- Group therapy<br/>
- Family therapy<br/><br/>

Medications:<br/>
- Antidepressants<br/>
- Anti-anxiety medications<br/>
- Mood stabilizers<br/>
- Antipsychotics<br/><br/>

<b>Self-Care Strategies:</b><br/>
- Regular exercise<br/>
- Healthy sleep schedule<br/>
- Balanced diet<br/>
- Social connections<br/>
- Relaxation techniques (meditation, yoga)<br/>
- Limiting alcohol and drugs<br/>
- Spending time in nature<br/>
- Creative activities<br/>
- Setting boundaries<br/><br/>

<b>When to Seek Help:</b><br/>
- Persistent sadness or worry<br/>
- Loss of interest in activities<br/>
- Changes in sleep or appetite<br/>
- Difficulty concentrating<br/>
- Thoughts of self-harm<br/><br/>

Remember: Seeking help is a sign of strength, not weakness. Recovery is possible."""
    },
    {
        "filename": "respiratory_health.pdf",
        "title": "Respiratory Health and Diseases",
        "content": """<b>RESPIRATORY HEALTH AND DISEASES</b><br/><br/>
<b>Understanding the Respiratory System:</b><br/>
The respiratory system includes the nose, trachea, lungs, and diaphragm. It's responsible for gas exchange and breathing.<br/><br/>

<b>Common Respiratory Conditions:</b><br/>
Asthma: Chronic inflammatory disease of airways, symptoms include wheezing and shortness of breath, triggered by allergens and exercise<br/><br/>

COPD: Progressive disease affecting breathing, includes emphysema and chronic bronchitis, usually caused by smoking<br/><br/>

Pneumonia: Infection causing inflammation in lungs, can be bacterial, viral, or fungal<br/><br/>

Bronchitis: Inflammation of airways in lungs, acute or chronic, causes persistent cough<br/><br/>

Lung Cancer: Leading cancer death in smokers and non-smokers, risk factors include smoking and secondhand smoke<br/><br/>

<b>Risk Factors:</b><br/>
- Smoking and secondhand smoke<br/>
- Air pollution<br/>
- Occupational exposure (dust, chemicals)<br/>
- Infections<br/>
- Genetics<br/>
- Age<br/>
- Indoor air quality<br/><br/>

<b>Prevention:</b><br/>
- Don't smoke (or quit)<br/>
- Avoid secondhand smoke<br/>
- Reduce air pollution exposure<br/>
- Get vaccinated (flu, pneumonia)<br/>
- Maintain clean home environment<br/>
- Use air purifiers<br/>
- Regular exercise<br/>
- Healthy diet<br/><br/>

<b>Symptoms Requiring Medical Attention:</b><br/>
- Persistent cough lasting 3+ weeks<br/>
- Coughing up blood<br/>
- Shortness of breath at rest<br/>
- Chest pain<br/>
- Fever"""
    }
]


def create_pdf_with_reportlab(filename: str, title: str, html_content: str):
    """Create a PDF using reportlab."""
    filepath = f"data/medical_pdfs/{filename}"

    # Create the PDF
    pdf = SimpleDocTemplate(filepath, pagesize=letter)
    story = []

    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#000080',
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=12
    )

    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2*inch))

    # Add content
    story.append(Paragraph(html_content, body_style))

    # Build PDF
    pdf.build(story)
    print(f"✅ Created: {filename}")


def main():
    """Create all sample medical PDFs."""
    print("\n" + "=" * 60)
    print("📝 Generating Medical PDFs with Reportlab")
    print("=" * 60 + "\n")

    # Create data directory
    Path("data/medical_pdfs").mkdir(parents=True, exist_ok=True)

    # Create each PDF
    for doc in MEDICAL_DOCUMENTS:
        create_pdf_with_reportlab(doc["filename"], doc["title"], doc["content"])

    # Display statistics
    total_size = 0
    pdf_files = [f for f in os.listdir("data/medical_pdfs") if f.endswith(".pdf")]

    print("\n" + "=" * 60)
    print("📊 Created Files Summary")
    print("=" * 60)
    print(f"Total Files: {len(pdf_files)}\n")

    for pdf in sorted(pdf_files):
        filepath = os.path.join("data/medical_pdfs", pdf)
        size = os.path.getsize(filepath) / 1024  # KB
        total_size += size
        print(f"  • {pdf:<40} {size:>10.2f} KB")

    print(f"\n📊 Total Size: {total_size/1024:.2f} MB")
    print("=" * 60 + "\n")

    print("✅ All medical PDFs generated successfully!")
    print("📁 Location: data/medical_pdfs/\n")


if __name__ == "__main__":
    main()
