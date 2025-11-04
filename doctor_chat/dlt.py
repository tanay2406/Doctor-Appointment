import google.generativeai as genai
genai.configure(api_key="AIzaSyAF-B9VLvbdpgVPdUWEjZPDg-PWsSoAOB8")

for m in genai.list_models():
    print(m.name)
