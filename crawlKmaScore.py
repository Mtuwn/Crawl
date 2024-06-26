import requests
import json
import time

all_students = []
so = 180101
print("Processing, please wait!!!")


while so < 200000:    
    for i in range(700):
        temp = so
        temp += i
        msv = "AT" + f"{temp}"
        print(msv)
        url = f"https://score.superkma.com/_next/data/u2WvndqTK-sVL8baZcHG4/student/{msv}.json?id={msv}"
        
        attempt = 0
        
        response = requests.get(url)
        print(response.status_code)
        # if response.status_code == 200:
        #     break 
        # else:Q
        #     attempt += 1
        #     time.sleep(1) 
        
        if response.status_code != 200:
            continue
        
        try:
            data = json.loads(response.text)
            student_name = data['pageProps']['data']['name']
            avg_score = data['pageProps']['data']['avgScore']
            passed_subjects = data['pageProps']['data']['passedSubjects']
            failed_subjects = data['pageProps']['data']['failedSubjects']
            class_name = data['pageProps']['data']['class']

            data_student = {
                "avgScore": avg_score,
                "class": class_name,
                "name": student_name,
                "failedSubjects": failed_subjects,
                "passedSubjects": passed_subjects
            }
            all_students.append(data_student)
        except Exception as e:
            print(f"Error processing data for student {msv}: {e}")

    so += 10000

json_str = json.dumps(all_students, indent=4, ensure_ascii=False)
with open('students.json', 'w', encoding='utf-8') as file:
    file.write(json_str)

print("Data retrieval and JSON generation completed!")
