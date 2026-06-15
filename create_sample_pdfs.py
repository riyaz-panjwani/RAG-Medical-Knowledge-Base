#!/usr/bin/env python3
"""
Create sample medical PDF files for testing the RAG system.
"""

import os
from fpdf import FPDF
from pathlib import Path

# Medical content for PDFs
MEDICAL_DOCUMENTS = [
    {
        "filename": "diabetes_overview.pdf",
        "title": "Diabetes Overview",
        "content": """DIABETES OVERVIEW

What is Diabetes?
Diabetes is a chronic condition that affects how your body processes blood sugar (glucose). There are three main types of diabetes: Type 1, Type 2, and Gestational diabetes.

Type 1 Diabetes:
- Autoimmune condition where pancreas doesn't produce insulin
- Typically diagnosed in children and young adults
- Requires daily insulin injections or pump therapy

Type 2 Diabetes:
- Most common form (90-95% of cases)
- Body doesn't use insulin effectively (insulin resistance)
- Often associated with obesity and sedentary lifestyle
- Can often be managed with lifestyle changes and medication

Symptoms:
- Increased thirst
- Frequent urination
- Fatigue
- Blurred vision
- Slow healing of cuts or wounds

Risk Factors:
- Family history of diabetes
- Obesity
- Physical inactivity
- Poor diet high in sugar and processed foods
- Age over 45 years old

Management:
- Blood sugar monitoring
- Healthy diet and exercise
- Medication (if prescribed)
- Regular medical checkups
- Stress management

Complications:
- Heart disease and stroke
- Kidney disease
- Vision problems (diabetic retinopathy)
- Nerve damage (neuropathy)
- Foot problems

Prevention:
- Maintain healthy weight
- Exercise regularly (150 minutes per week)
- Eat healthy diet rich in vegetables
- Reduce sugar and processed food intake
- Get regular checkups"""
    },
    {
        "filename": "hypertension_management.pdf",
        "title": "Hypertension Management",
        "content": """HYPERTENSION MANAGEMENT GUIDE

What is High Blood Pressure?
Hypertension, or high blood pressure, is a common condition where the force of blood against artery walls is too high, usually 140/90 mmHg or higher.

Blood Pressure Categories:
- Normal: Less than 120/80 mmHg
- Elevated: Systolic 120-129 and Diastolic less than 80
- Stage 1 Hypertension: Systolic 130-139 or Diastolic 80-89
- Stage 2 Hypertension: Systolic 140 or higher or Diastolic 90 or higher

Causes:
Primary Hypertension (90-95% of cases):
- No identifiable secondary cause
- Often related to genetics, age, and lifestyle factors

Secondary Hypertension:
- Kidney disease
- Thyroid problems
- Sleep apnea
- Certain medications

Risk Factors:
- Age (risk increases with age)
- Family history
- Obesity
- Excessive alcohol use
- High sodium diet
- Stress
- Physical inactivity

Treatment Options:
Lifestyle Changes:
- DASH diet (low sodium, high potassium)
- Regular aerobic exercise (150 minutes/week)
- Weight loss if overweight
- Limit alcohol
- Stress management
- Quit smoking

Medications:
- ACE inhibitors
- Beta-blockers
- Calcium channel blockers
- Diuretics
- ARBs (Angiotensin II receptor blockers)

Prevention:
- Check blood pressure regularly
- Keep a blood pressure log
- Home monitoring devices
- Regular doctor visits"""
    },
    {
        "filename": "heart_disease_prevention.pdf",
        "title": "Heart Disease Prevention",
        "content": """HEART DISEASE PREVENTION

Heart Disease Facts:
Heart disease is the leading cause of death in the United States. Prevention is crucial and can significantly reduce risk.

Types of Heart Disease:
1. Coronary Artery Disease (CAD)
   - Most common type
   - Plaque buildup in arteries
   - Can lead to heart attack

2. Heart Failure
   - Heart can't pump enough blood
   - Can be caused by high blood pressure, CAD, diabetes

3. Arrhythmias
   - Irregular heartbeat
   - Can be life-threatening

4. Valvular Heart Disease
   - Problems with heart valves
   - Can be congenital or acquired

Risk Factors You Cannot Change:
- Age
- Sex
- Family history
- Race/ethnicity

Risk Factors You Can Change:
- High blood pressure
- High cholesterol
- Smoking
- Obesity
- Physical inactivity
- Diabetes
- Stress

Prevention Strategies:

Nutrition:
- Mediterranean diet
- Limit saturated fats (less than 5% of calories)
- Eliminate trans fats
- Increase fiber (25-30g daily)
- Limit sodium to less than 2,300mg daily

Exercise:
- 150 minutes of moderate aerobic activity per week
- Strength training 2 days per week
- Flexibility exercises

Screening:
- Cholesterol screening every 4-6 years
- Blood pressure monitoring
- Blood sugar screening
- EKG if symptoms present

Signs of Heart Attack:
- Chest pain or pressure
- Shortness of breath
- Pain in arm, neck, jaw
- Nausea or dizziness

Action: Call 911 immediately if experiencing these symptoms"""
    },
    {
        "filename": "mental_health_wellbeing.pdf",
        "title": "Mental Health and Wellbeing",
        "content": """MENTAL HEALTH AND WELLBEING

What is Mental Health?
Mental health includes emotional, psychological, and social wellbeing. It's as important as physical health.

Common Mental Health Conditions:

Depression:
- Persistent sadness and loss of interest
- Affects daily functioning
- More than just being sad
- Treatable with therapy and/or medication

Anxiety Disorders:
- Excessive worry and fear
- Physical symptoms: racing heart, sweating
- Can be generalized or specific (phobias, panic)

Risk Factors:
- Genetics/family history
- Brain chemistry
- Trauma or adverse events
- Chronic stress
- Substance abuse
- Medical conditions
- Social isolation

Support and Treatment:

Therapy Options:
- Cognitive Behavioral Therapy (CBT)
- Psychotherapy
- Group therapy
- Family therapy

Medications:
- Antidepressants
- Anti-anxiety medications
- Mood stabilizers
- Antipsychotics

Self-Care Strategies:
- Regular exercise
- Healthy sleep schedule
- Balanced diet
- Social connections
- Relaxation techniques (meditation, yoga)
- Limiting alcohol and drugs
- Spending time in nature
- Creative activities
- Setting boundaries

When to Seek Help:
- Persistent sadness or worry
- Loss of interest in activities
- Changes in sleep or appetite
- Difficulty concentrating
- Thoughts of self-harm

Getting Help:
- Talk to your doctor
- See a therapist or counselor
- Call a mental health crisis line
- Reach out to trusted friends/family

Remember: Seeking help is a sign of strength, not weakness. Recovery is possible."""
    },
    {
        "filename": "respiratory_health.pdf",
        "title": "Respiratory Health and Diseases",
        "content": """RESPIRATORY HEALTH AND DISEASES

Understanding the Respiratory System:
The respiratory system includes the nose, trachea, lungs, and diaphragm. It's responsible for gas exchange and breathing.

Common Respiratory Conditions:

Asthma:
- Chronic inflammatory disease of airways
- Symptoms: wheezing, coughing, shortness of breath
- Triggered by allergens, exercise, stress, cold air
- Managed with inhalers and medications

COPD (Chronic Obstructive Pulmonary Disease):
- Progressive disease affecting breathing
- Includes emphysema and chronic bronchitis
- Usually caused by smoking
- Characterized by airflow limitation

Pneumonia:
- Infection causing inflammation in lungs
- Can be bacterial, viral, or fungal
- Symptoms: cough, fever, shortness of breath
- Requires prompt treatment

Bronchitis:
- Inflammation of airways in lungs
- Acute or chronic
- Causes persistent cough
- Often follows upper respiratory infection

Lung Cancer:
- Leading cancer death in smokers and non-smokers
- Risk factors: smoking, secondhand smoke, radon
- Symptoms: persistent cough, chest pain, shortness of breath
- Early detection improves outcomes

Risk Factors:
- Smoking and secondhand smoke
- Air pollution
- Occupational exposure (dust, chemicals)
- Infections
- Genetics
- Age
- Indoor air quality

Prevention:
- Don't smoke (or quit)
- Avoid secondhand smoke
- Reduce air pollution exposure
- Get vaccinated (flu, pneumonia)
- Maintain clean home environment
- Use air purifiers
- Regular exercise
- Healthy diet

Symptoms Requiring Medical Attention:
- Persistent cough lasting 3+ weeks
- Coughing up blood
- Shortness of breath at rest
- Chest pain
- Fever"""
    }
]


def create_pdf(filename: str, title: str, content: str):
    """Create a PDF file with medical content."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    # Add title
    pdf.set_font("Helvetica", "B", size=14)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Add content with proper text handling
    pdf.set_font("Helvetica", size=10)
    for line in content.split('\n'):
        if line.strip():
            # Simple text wrapping for long lines
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if pdf.get_string_width(test_line) < 180:
                    current_line = test_line
                else:
                    if current_line:
                        pdf.cell(0, 5, current_line.strip(), new_x="LMARGIN", new_y="NEXT")
                    current_line = word + " "
            if current_line:
                pdf.cell(0, 5, current_line.strip(), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.ln(2)

    filepath = f"data/medical_pdfs/{filename}"
    pdf.output(filepath)
    print(f"✅ Created: {filename}")


def main():
    """Create all sample medical PDFs."""
    print("\n" + "=" * 60)
    print("📝 Creating Sample Medical PDFs")
    print("=" * 60 + "\n")

    # Create data directory
    Path("data/medical_pdfs").mkdir(parents=True, exist_ok=True)

    # Create each PDF
    for doc in MEDICAL_DOCUMENTS:
        create_pdf(doc["filename"], doc["title"], doc["content"])

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

    print("✅ All sample PDFs created successfully!")
    print("📁 Location: data/medical_pdfs/\n")


if __name__ == "__main__":
    main()
