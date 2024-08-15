Downloads:
axios
pip
pip install Flask
pip install PyMuPDF
pip install scikit-learn
pip install requests



ats_service.py

from io import BytesIO

import fitz  # PyMuPDF
import requests
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(url):
    try:
        url = url.replace("\\", "/")
        response = requests.get(url)
        response.raise_for_status()
        pdf_data = BytesIO(response.content)
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except fitz.FitzError as e:
        return f"PDF processing error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def calculate_similarity(resume_text, job_description, job_skills):
    # Combine job description and job skills into one document
    combined_job_details = job_description + " " + job_skills
    
    documents = [resume_text, combined_job_details]
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return similarity[0][0]  # Return the similarity score

app = Flask(__name__)

@app.route('/process-data', methods=['POST'])
def process_data():
    data = request.json
    resume_url = data.get('resume_url')
    job_description = data.get('job_description')
    job_skills = data.get('job_skills')

    if not resume_url or not job_description or not job_skills:
        return jsonify({'error': 'resume_url, job_description, and job_skills are required'}), 400

    resume_text = extract_text_from_pdf(resume_url)
    if resume_text.startswith("Request error") or resume_text.startswith("PDF processing error") or resume_text.startswith("An unexpected error occurred"):
        return jsonify({'error': resume_text}), 400

    similarity_score = calculate_similarity(resume_text, job_description, job_skills)

    ats_score = round(similarity_score * 100, 2)

    return jsonify({'ats_score': ats_score})

if __name__ == "__main__":
    app.run(port=5001, debug=True)



Route: 

  app.post('/user-apply-job', upload.fields([{ name: 'resume', maxCount: 1 }, { name: 'proofs', maxCount: 10 }]), async (req, res) => {
    const {
        name,
        gender,
        email,
        phoneNo,
        age,
        education,
        experience,
        j_id,
        c_registrationNo,
        js_id
    } = req.body;

    const resume = req.files['resume'][0].path;
    const proofs = req.files['proofs'].map(file => file.path);

    try {
        // Retrieve job description and skills from the database
        const jobQuery = `
            SELECT j.job_description, GROUP_CONCAT(js.skill) AS job_skills
            FROM jobs j
            JOIN job_skills js ON j.j_id = js.j_id
            WHERE j.j_id = ?
            GROUP BY j.j_id;
        `;
        
        db.query(jobQuery, [j_id], async (err, jobResult) => {
            if (err || jobResult.length === 0) {
                console.error('Error fetching job details:', err || 'Job not found');
                return res.status(500).send('Error fetching job details');
            }

            const { job_description, job_skills } = jobResult[0];

            // Prepare the data to send to the Python ATS
            const applicantData = {
                name,
                gender,
                email,
                phoneNo,
                age,
                education,
                experience,
                j_id,
                c_registrationNo,
                js_id,
                resume_url: `http://localhost:3001/${resume}`,
                job_description: job_description,
                job_skills: job_skills
            };

            // Send data to Python ATS for processing
            const atsResponse = await axios.post('http://127.0.0.1:5001/process-data', applicantData);
            const atsScore = atsResponse.data.ats_score;

            // Insert applicant data into the applicant table
            db.query('INSERT INTO applicant (app_resume, app_gender, app_name, app_email, app_age, app_education, app_experience, app_phoneNo, j_id, c_registrationNo, ats_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                [resume, gender, name, email, age, education, experience, phoneNo, j_id, c_registrationNo, atsScore], (error, results) => {
                if (error) {
                    console.error('Error inserting applicant data:', error);
                    return res.status(500).send('Error inserting applicant data');
                }

                const appId = results.insertId;

                const proofValues = proofs.map(proof => [appId, proof]);

                // Insert proofs into the proofs table
                db.query('INSERT INTO proofs (app_id, proof) VALUES ?', [proofValues], (error) => {
                    if (error) {
                        console.error('Error inserting proofs:', error);
                        return res.status(500).send('Error inserting proofs');
                    }

                    // Insert data into apply table
                    const applyQuery = 'INSERT INTO apply (js_id, j_id) VALUES (?, ?)';
                    db.query(applyQuery, [js_id, j_id], (err, result) => {
                        if (err) {
                            console.error('Error inserting into apply table:', err);
                            return res.status(500).send('Error submitting data into apply table');
                        }
                        res.status(200).send('Application submitted successfully with ATS score');
                    });
                });
            });
        });
    } catch (error) {
        console.error('Error communicating with Python server:', error);
        res.status(500).send('Error processing application');
    }
});
