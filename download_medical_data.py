#!/usr/bin/env python3
"""
Download sample medical PDFs from public sources for the RAG system.
"""

import sys
import logging
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_manager import DataManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Medical PDF sources (public domain or open access)
MEDICAL_PDF_SOURCES = [
    {
        "name": "NIH_Diabetes_Overview.pdf",
        "url": "https://www.niddk.nih.gov/health-information/health-topics/diabetes",
        "description": "Overview of diabetes from NIH"
    },
    {
        "name": "WHO_Hypertension_Guidelines.pdf",
        "url": "https://apps.who.int/iris/handle/10665/272564",
        "description": "WHO Guidelines on Hypertension"
    },
    {
        "name": "Heart_Disease_Overview.pdf",
        "url": "https://www.heart.org/en/health-topics/heart-attack",
        "description": "Heart disease information from American Heart Association"
    },
    {
        "name": "COVID19_Health_Info.pdf",
        "url": "https://www.cdc.gov/coronavirus/2019-ncov/index.html",
        "description": "COVID-19 health information from CDC"
    },
    {
        "name": "Mental_Health_Guide.pdf",
        "url": "https://www.samhsa.gov/mental-health",
        "description": "Mental health resources from SAMHSA"
    }
]

# Alternative: Direct PDF links from reliable sources
DIRECT_PDF_LINKS = [
    {
        "name": "clinical_practice_guidelines.pdf",
        "url": "https://www.ncbi.nlm.nih.gov/pmc/",
        "description": "Clinical practice guidelines from PubMed Central"
    }
]


def create_sample_pdfs():
    """Create sample medical documents locally for testing."""
    data_manager = DataManager()

    sample_documents = [
        {
            "filename": "diabetes_overview.pdf",
            "title": "Diabetes Overview",
            "content": """
DIABETES OVERVIEW

What is Diabetes?
Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).
There are three main types of diabetes: Type 1, Type 2, and Gestational diabetes.

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
- Get regular checkups
"""
        },
        {
            "filename": "hypertension_management.pdf",
            "title": "Hypertension Management",
            "content": """
HYPERTENSION MANAGEMENT GUIDE

What is High Blood Pressure?
Hypertension, or high blood pressure, is a common condition where the force of blood
against artery walls is too high, usually 140/90 mmHg or higher.

Blood Pressure Categories:
- Normal: Less than 120/80 mmHg
- Elevated: Systolic 120-129 and Diastolic less than 80
- Stage 1 Hypertension: Systolic 130-139 or Diastolic 80-89
- Stage 2 Hypertension: Systolic 140 or higher or Diastolic 90 or higher
- Hypertensive Crisis: Systolic higher than 180 and/or Diastolic higher than 120

Causes:
Primary Hypertension (90-95% of cases):
- No identifiable secondary cause
- Often related to genetics, age, and lifestyle factors

Secondary Hypertension:
- Kidney disease
- Thyroid problems
- Sleep apnea
- Certain medications

Symptoms:
Many people with hypertension have no symptoms. High blood pressure is often called
the "silent killer" because damage occurs without awareness.

When symptoms occur:
- Headaches
- Shortness of breath
- Nosebleeds
- Chest pain

Risk Factors:
- Age (risk increases with age)
- Family history
- Obesity
- Excessive alcohol use
- High sodium diet
- Stress
- Physical inactivity

Treatment Options:
Lifestyle Changes (First-line treatment):
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

Monitoring:
- Check blood pressure regularly
- Keep a blood pressure log
- Home monitoring devices
- Regular doctor visits

Complications if Untreated:
- Heart attack
- Stroke
- Heart failure
- Kidney disease
- Vision loss
"""
        },
        {
            "filename": "heart_disease_prevention.pdf",
            "title": "Heart Disease Prevention",
            "content": """
HEART DISEASE PREVENTION

Heart Disease Facts:
Heart disease is the leading cause of death in the United States.
Prevention is crucial and can significantly reduce risk.

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
- Choose lean proteins
- Eat plenty of fruits and vegetables

Exercise:
- 150 minutes of moderate aerobic activity per week
- Strength training 2 days per week
- Flexibility exercises

Other Prevention Measures:
- Don't smoke (or quit if you do)
- Manage stress
- Get adequate sleep (7-9 hours)
- Maintain healthy weight
- Control diabetes
- Manage high blood pressure
- Know your cholesterol levels

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

Action: Call 911 immediately if experiencing these symptoms
"""
        },
        {
            "filename": "mental_health_wellbeing.pdf",
            "title": "Mental Health and Wellbeing",
            "content": """
MENTAL HEALTH AND WELLBEING

What is Mental Health?
Mental health includes emotional, psychological, and social wellbeing.
It's as important as physical health.

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

Bipolar Disorder:
- Extreme mood swings
- Episodes of depression and mania
- Requires professional treatment

Schizophrenia:
- Affects perception of reality
- Hallucinations and delusions
- Requires ongoing management

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
- Substance abuse

Getting Help:
- Talk to your doctor
- See a therapist or counselor
- Call a mental health crisis line
- Reach out to trusted friends/family
- Consider support groups

Remember:
- Mental health is part of overall health
- Seeking help is a sign of strength, not weakness
- Recovery is possible
- You are not alone
"""
        },
        {
            "filename": "respiratory_health.pdf",
            "title": "Respiratory Health and Diseases",
            "content": """
RESPIRATORY HEALTH AND DISEASES

Understanding the Respiratory System:
The respiratory system includes the nose, trachea, lungs, and diaphragm.
It's responsible for gas exchange and breathing.

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

Allergies:
- Immune system overreaction to harmless substances
- Can be seasonal or year-round
- Treated with antihistamines and avoidance

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
- Fever

Diagnosis:
- Physical examination
- Chest X-ray
- CT scan
- Spirometry (lung function tests)
- Blood tests
- Bronchoscopy

Treatment Options:
- Medications (inhalers, oral medications)
- Oxygen therapy
- Pulmonary rehabilitation
- Lifestyle modifications
- Surgery (if necessary)
"""
        }
    ]

    print("\n📝 Creating sample medical PDFs for testing...\n")

    for doc in sample_documents:
        filepath = f"data/medical_pdfs/{doc['filename']}"
        try:
            with open(filepath, "w") as f:
                f.write(doc["title"] + "\n")
                f.write("=" * 50 + "\n")
                f.write(doc["content"])

            logger.info(f"✅ Created: {doc['filename']}")
        except Exception as e:
            logger.error(f"❌ Error creating {doc['filename']}: {str(e)}")

    return data_manager


def main():
    """Main function to download and organize medical data."""
    print("\n" + "=" * 60)
    print("🏥 MEDICAL DATA DOWNLOADER")
    print("=" * 60)

    data_manager = DataManager()

    # Create sample PDFs for testing
    print("\n📚 Creating sample medical documents...")
    data_manager = create_sample_pdfs()

    # Display statistics
    data_manager.display_statistics()

    # Validate PDFs
    print("🔍 Validating PDFs...")
    results = data_manager.validate_pdfs()
    data_manager.display_validation_results(results)

    # Save catalog
    stats = data_manager.get_data_statistics()
    data_manager.save_catalog(stats)

    print("✅ Data setup complete!")
    print(f"📁 PDFs saved to: data/medical_pdfs/")
    print(f"📊 Catalog saved to: data/medical_pdfs/catalog.json\n")


if __name__ == "__main__":
    main()
