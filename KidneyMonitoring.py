import numpy as np
import pandas as pd
import streamlit as st
import joblib
from lime.lime_tabular import LimeTabularExplainer
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from sklearn.preprocessing import LabelEncoder
import openai


def get_gpt_recommendations(egfr_category, features):
    # Prepare the input text for GPT
    input_text = f"The patient's eGFR category is {egfr_category}. Here are the feature values: \n"
    for feature_name, value in features.items():
        input_text += f"{feature_name}: {value}\n"
    input_text += "Please provide personalized recommendations to improve the patient's kidney health."

    # Call GPT-3.5 API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing health recommendations based on user inputs."},
            {"role": "user", "content": input_text}
        ]
    )
    # Extract recommendations from the GPT-3 response
    recommendations = response['choices'][0]['message']['content'].strip()
    return recommendations

def monitor_kidney_page():
    st.title('📑 Monitor Kidney Function')
    st.markdown("Evaluate your kidney function here.")
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'monitor_kidney'    # Load your trained model
    
    with open('Model/v_best_ada.joblib','rb') as model_path:  # Ensure the path is correct and enclosed in quotes
        model = joblib.load(model_path)

    # Load training data from CSV file
    training_data_path = 'vif.csv'  # Adjust path as needed
    df = pd.read_csv(training_data_path)
    df = df.drop('egfr_categories', axis=1)

    def hypertension_status(systolic, diastolic):
        return (systolic >= 130 or diastolic >= 80)

    def anemia_status(hemoglobin):
        return hemoglobin < 12

    # Define feature names and classes for LIME
    feature_names = df.columns.tolist()

    class_names = ['Stage 1', 'Stage 2', 'Stage 3',
                    'Stage 4','Stage 5']

    # Initialize the explainer
    explainer = LimeTabularExplainer(
        training_data=df.values,  
        feature_names=feature_names,
        class_names=class_names,
        mode='classification'
        )

   # Create a form for the sliders
    with st.form(key='kidney_form'):
        serum_creatinine = st.slider("Serum Creatinine (mg/dL)", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
        bun = st.slider("BUN (mg/dL)", min_value=5.0, max_value=20.0, value=12.5, step=0.1,
                        help="Blood Urea Nitrogen")
        uacr = st.number_input("UACR (mg/g)", min_value=0.0, max_value=300.0, value=150.0, step=0.1,
                         help="Urine Albumin to Creatinine Ratio")    
        urine_output = st.slider("Urine Output (L/day)", min_value=0.5, max_value=2.0, value=1.25, step=0.1)
        sodium = st.slider("Sodium (mmol/L)", min_value=135.0, max_value=145.0, value=140.0, step=0.1)
        potassium = st.slider("Potassium (mmol/L)", min_value=3.5, max_value=5.0, value=4.25, step=0.1)
        hemoglobin = st.slider("Hemoglobin (g/dL)", min_value=10.0, max_value=15.0, value=12.5, step=0.1)
        systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", min_value=90, max_value=180, value=135, step=1)
        diastolic_bp = st.slider("Diastolic Blood Pressure (mmHg)", min_value=60, max_value=120, value=90, step=1)
        submit_button = st.form_submit_button(label='Check Kidney Health')

    if submit_button:
        st.session_state['current_page'] = 'monitor_kidney'
        hypertension = hypertension_status(systolic_bp, diastolic_bp)
        anemia = anemia_status(hemoglobin)
                
        features = pd.DataFrame([[serum_creatinine, bun, uacr, urine_output, sodium,
                                  potassium,hemoglobin, systolic_bp, diastolic_bp, 
                                  hypertension, anemia]],
                        columns=feature_names)
        
        egfr_categories = model.predict(features)
        st.write("Predicted Kidney Health: ")
        st.markdown(f"""
            <style>
            .big-font {{
                font-size:30px !important;
            }}
            </style>
            <p class="big-font">{egfr_categories[0]}</p>
            """, unsafe_allow_html=True)
        image_path = "StagesImage.jpg"
        st.image(image_path)

        # Generate and display LIME explanation
        exp = explainer.explain_instance(
            num_features=len(feature_names),
            top_labels=1,
            data_row=features.iloc[0],
            predict_fn=model.predict_proba
        )
            
        explanation_html = exp.as_html()

        # Display the explanation for each class
        st.markdown("### LIME Explanation")
        components.html(explanation_html, height=800, scrolling=False)
        
        # Prepare features dictionary for GPT-3
        features_dict = {
            "Serum Creatinine": serum_creatinine,
            "BUN": bun,
            "UACR": uacr,
            "Urine Output": urine_output,
            "Sodium": sodium,
            "Potassium": potassium,
            "Hemoglobin": hemoglobin,
            "Systolic Blood Pressure": systolic_bp,
            "Diastolic Blood Pressure": diastolic_bp,
            "Hypertension": hypertension,
            "Anemia": anemia
        }

        # Get recommendations from GPT-3
        recommendations = get_gpt_recommendations(egfr_categories, features_dict)
        st.header("Recommendations for Improvement")
        st.write(recommendations)
