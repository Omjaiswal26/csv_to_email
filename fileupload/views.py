from django.shortcuts import render
import pandas as pd
from .models import File
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def home(request):
    message = "Enter CSV or Excel only"
    if request.method == 'POST':
        recipient = request.POST.get('email')
        file = request.FILES['file']
        if str(file).endswith('.xlsx') or str(file).endswith('.csv'):
            file_obj = File.objects.create(file = file)
            message = "Success"
            if str(file).endswith('.xlsx'):
                df = pd.read_excel(file_obj.file)
            else:
                df = pd.read_csv(file_obj.file)
            grouped_df = df.groupby(['Cust State', 'DPD']).size()

            summary_report = grouped_df.reset_index(name='Count')
            summary_report.columns = ['State', 'DPD', 'Count']

            html_table = summary_report.to_html(index=False)
            context ={
                'html_table':html_table,
            }

            subject = 'Python(Django) Assignment - Om Jaiswal'
            email_from = 'work.omjaiswal@gmail.com'
            recipient_list = [recipient]

            # Render email template with DataFrame HTML content
            email_template = 'data.html'
            context = {'content': html_table}
            email_message = render_to_string(email_template, context)

            # Send email
            email = EmailMessage(subject, email_message, email_from, recipient_list)
            email.content_subtype = 'html'  # Set content type to HTML
            email.send()
            print("EMAIL SENT SUCCCESSFULLY")
            return render(request, 'data.html', context)
        else:
            message = "File should be Excel or CSV"
    return render(request, 'home.html', {'message': message})