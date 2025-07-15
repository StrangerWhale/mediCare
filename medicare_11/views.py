from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from appointments.models import DiseaseSearch
import json

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def search_disease(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            
            if not query:
                return JsonResponse({'error': 'Please enter a disease or symptom to search'})
            
            # Simple AI-like response based on common diseases/symptoms
            response = get_disease_info(query.lower())
            
            # Save search to database
            patient = None
            if request.user.is_authenticated and hasattr(request.user, 'patient'):
                patient = request.user.patient
            
            DiseaseSearch.objects.create(
                query=query,
                response=response,
                patient=patient
            )
            
            return JsonResponse({
                'success': True,
                'response': response,
                'query': query
            })
            
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while processing your request'})
    
    return JsonResponse({'error': 'Invalid request method'})

def get_disease_info(query):
    """Simple disease information lookup - in production, this would use a real AI API"""
    
    disease_info = {
        'fever': {
            'info': 'Fever is a temporary increase in body temperature, often due to an illness. Common causes include infections, heat exhaustion, and certain medications.',
            'symptoms': 'High body temperature, chills, sweating, headache, muscle aches',
            'recommendations': 'Rest, stay hydrated, take fever reducers if needed. Consult a doctor if fever persists or is very high.',
            'specialists': 'General Physician, Internal Medicine'
        },
        'headache': {
            'info': 'Headaches are pain in the head or upper neck. They can be primary (not caused by another condition) or secondary (symptom of another condition).',
            'symptoms': 'Pain in head, neck, or scalp; may be throbbing, sharp, or dull',
            'recommendations': 'Rest in a quiet, dark room. Stay hydrated. Over-the-counter pain relievers may help.',
            'specialists': 'Neurologist, General Physician'
        },
        'cough': {
            'info': 'A cough is a reflex action to clear the airways of mucus and irritants. It can be acute (short-term) or chronic (long-term).',
            'symptoms': 'Dry or productive cough, throat irritation, chest discomfort',
            'recommendations': 'Stay hydrated, use honey for throat soothing, avoid irritants. See a doctor if persistent.',
            'specialists': 'Pulmonologist, General Physician'
        },
        'diabetes': {
            'info': 'Diabetes is a group of metabolic disorders characterized by high blood sugar levels over a prolonged period.',
            'symptoms': 'Frequent urination, increased thirst, unexplained weight loss, fatigue, blurred vision',
            'recommendations': 'Monitor blood sugar, maintain healthy diet, regular exercise, take prescribed medications.',
            'specialists': 'Endocrinologist, Diabetologist'
        },
        'hypertension': {
            'info': 'High blood pressure (hypertension) is a condition where blood pressure in the arteries is persistently elevated.',
            'symptoms': 'Often no symptoms (silent killer), may cause headaches, shortness of breath, nosebleeds',
            'recommendations': 'Regular monitoring, low-sodium diet, regular exercise, stress management, medication if prescribed.',
            'specialists': 'Cardiologist, General Physician'
        },
        'asthma': {
            'info': 'Asthma is a respiratory condition where airways narrow and swell, producing extra mucus, making breathing difficult.',
            'symptoms': 'Shortness of breath, chest tightness, wheezing, coughing',
            'recommendations': 'Avoid triggers, use prescribed inhalers, have an action plan, regular check-ups.',
            'specialists': 'Pulmonologist, Allergist'
        }
    }
    
    # Check for exact matches first
    for disease, info in disease_info.items():
        if disease in query:
            return format_disease_response(disease.title(), info)
    
    # Check for symptom matches
    symptom_keywords = {
        'pain': 'headache',
        'ache': 'headache',
        'temperature': 'fever',
        'hot': 'fever',
        'cold': 'fever',
        'breathing': 'asthma',
        'breath': 'asthma',
        'wheeze': 'asthma',
        'sugar': 'diabetes',
        'thirst': 'diabetes',
        'urination': 'diabetes',
        'pressure': 'hypertension',
        'blood': 'hypertension'
    }
    
    for keyword, disease in symptom_keywords.items():
        if keyword in query and disease in disease_info:
            return format_disease_response(disease.title(), disease_info[disease])
    
    # Default response for unknown queries
    return """
    <div class="disease-info">
        <h5>General Health Information</h5>
        <p>I couldn't find specific information about your query. Here are some general recommendations:</p>
        <ul>
            <li>If you're experiencing persistent symptoms, consult a healthcare professional</li>
            <li>Maintain a healthy lifestyle with regular exercise and balanced diet</li>
            <li>Stay hydrated and get adequate sleep</li>
            <li>Don't ignore warning signs - seek medical attention when needed</li>
        </ul>
        <p><strong>For specific medical advice, please consult with a qualified healthcare provider.</strong></p>
    </div>
    """

def format_disease_response(disease_name, info):
    return f"""
    <div class="disease-info">
        <h5>{disease_name}</h5>
        <div class="info-section">
            <h6><i class="fas fa-info-circle text-primary"></i> Information</h6>
            <p>{info['info']}</p>
        </div>
        <div class="info-section">
            <h6><i class="fas fa-symptoms text-warning"></i> Common Symptoms</h6>
            <p>{info['symptoms']}</p>
        </div>
        <div class="info-section">
            <h6><i class="fas fa-recommendations text-success"></i> Recommendations</h6>
            <p>{info['recommendations']}</p>
        </div>
        <div class="info-section">
            <h6><i class="fas fa-user-md text-info"></i> Recommended Specialists</h6>
            <p>{info['specialists']}</p>
        </div>
        <div class="alert alert-warning mt-3">
            <small><i class="fas fa-exclamation-triangle"></i> This information is for educational purposes only. Please consult a healthcare professional for proper diagnosis and treatment.</small>
        </div>
    </div>
    """