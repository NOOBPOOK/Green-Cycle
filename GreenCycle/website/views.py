from django.shortcuts import render, HttpResponse
from website.models import Feedback, MetalRequest, PaperRequest, GlassRequest, PlasticRequest, ClothesRequest, EwasteRequest
import datetime
from google.oauth2.credentials import Credentials
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from pydantic import Field
from googleapiclient.discovery import Resource
from pydantic import BaseModel
import sqlite3
from sqlite3 import Error

FEEDBACK_MSG = """
We greatly value your opinion, and we're reaching out to request your valuable feedback on your recent experience with us.
Your insights will help us improve our services and provide you with a better experience.
"""

FEEDBACK_SUBJECT = "Thanks for your Feedback"

DEFAULT_SCOPES = ["https://mail.google.com/"]
DEFAULT_CREDS_TOKEN_FILE = "token.json"
DEFAULT_CLIENT_SECRETS_FILE = "C:/Users/hp/Documents/GitHub/Green-Cycle/credentials.json"

METALS = ["Aluminium","Brass","Copper","Alloy","Alloy Steel","Iron","Bronze","Ferrous","Other",""]
PAPER = ["Paper",""]
GLASS = ["Glass", ""]
PLASTIC = ["Miscellaneous Plastics", "Polistyrene Styrofoam", "Polypropylene", "Low-Density Polythylene", "Polyvinyl Chloride","High-Density Polythylene","Polyethylene Perephthalate",""]
EWASTE = ["Computer and telecommunication appliances","Small appliances","Major appliances",""]

def import_google():
    try:
        from google.auth.transport.requests import Request  # noqa: F401
        from google.oauth2.credentials import Credentials  # noqa: F401
    except ImportError:
        raise ImportError(
            "You need to install google-auth-httplib2 to use this toolkit. "
            "Try running pip install --upgrade google-auth-httplib2"
        )
    return Request, Credentials

def import_installed_app_flow():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ValueError(
            "You need to install google-auth-oauthlib to use this toolkit. "
            "Try running pip install --upgrade google-auth-oauthlib"
        )
    return InstalledAppFlow

def get_gmail_credentials(
    token_file: str = None,
    client_secrets_file: str = None,
    scopes = None,
    ) -> Credentials:
    """Get credentials."""
    # From https://developers.google.com/gmail/api/quickstart/python
    Request, Credentials = import_google()
    InstalledAppFlow = import_installed_app_flow()
    creds = None
    scopes = scopes or DEFAULT_SCOPES
    token_file = token_file or DEFAULT_CREDS_TOKEN_FILE
    client_secrets_file = client_secrets_file or DEFAULT_CLIENT_SECRETS_FILE
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application # noqa
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds

def import_googleapiclient_resource_builder():
    try:
        from googleapiclient.discovery import build
    except ImportError:
        raise ValueError(
            "You need to install googleapiclient to use this toolkit. "
            "Try running pip install --upgrade google-api-python-client"
        )
    return build

def build_resource_service(
    credentials: Credentials = None,
    service_name: str = "gmail",
    service_version: str = "v1",
    ) -> Resource:
    """Build a Gmail service."""
    credentials = credentials or get_gmail_credentials()
    builder = import_googleapiclient_resource_builder()
    return builder(service_name, service_version, credentials=credentials)

def sql_connect():
    name = MetalRequest._meta.db_table
    conn = None
    try:
        conn = sqlite3.connect("C:/Users/hp/Documents/GitHub/Green-Cycle/GreenCycle/db.sqlite3")
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {name}")
    row = cur.fetchall()
    for i in row:
        print(i)

class Gmail(BaseModel):
    api_resource: Resource = Field(default_factory=build_resource_service)

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    @classmethod
    def from_api_resource(cls, api_resource: Resource):
        return cls(service=api_resource)

    def _prepare_message(
        self,
        message: str,
        to: str,
        subject: str,
        cc = None,
        bcc = None,
        
    ):
        """Create a message for an email."""
        mime_message = MIMEMultipart()
        mime_message.attach(MIMEText(message, "html"))

        mime_message["To"] = ", ".join(to if isinstance(to, list) else [to])
        mime_message["Subject"] = subject

        if cc is not None:
            mime_message["Cc"] = ", ".join(cc if isinstance(cc, list) else [cc])
        if bcc is not None:
            mime_message["Bcc"] = ", ".join(bcc if isinstance(bcc, list) else [bcc])

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        return {"raw": encoded_message}

    def run(
        self,
        message: str,
        to: str,
        subject: str,
        cc = None,
        bcc = None,
    ) -> str:
        """Run the tool."""
        try:
            create_message = self._prepare_message(message, to, subject, cc, bcc)
            send_message = (
                self.api_resource.users().messages().send(userId="me", body=create_message))
            sent_message = send_message.execute()
            return f'Message sent. Message Id: {sent_message["id"]}'
        except Exception as error:
            raise Exception(f"An error occurred: {error}")

def home(request):
    sql_connect()
    if request.method == "POST":
        username = request.POST["usrname"]
        email = request.POST["usremail"]
        review = request.POST["feedback"]
        feedback = Feedback(name=username, 
                            email=email, 
                            feedback=review, 
                            date = datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=str(FEEDBACK_MSG), to=str(email), subject=FEEDBACK_SUBJECT)
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
        except Exception as e:
            print(f"One Error Occured {e}")
        return render(request, "index.html")
    else:
        return render(request, "index.html")

def paper(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        cate = request.POST["Category"]
        category = PAPER[int(cate)-1]
        desc = request.POST["message"]
        feedback = PaperRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category=category,
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the paper quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, "index.html")
    else:
        return render(request, "paper.html")

def clothes(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        category = []
        try:
            category.append(request.POST["clothes1"])
        except:
            pass
        try:
            category.append(request.POST["clothes2"])
        except:
            pass
        try:
            category.append(request.POST["clothes3"])
        except:
            pass
        try:
            category.append(request.POST["clothes4"])
        except:
            pass
        desc = request.POST["message"]
        feedback = ClothesRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category = ' ,'.join(category),
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the clothes quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, "index.html")
    else:
        return render(request, "clothes.html")

def plastic(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        cate = request.POST["Category"]
        category = PLASTIC[int(cate)-1]
        desc = request.POST["message"]
        feedback = PlasticRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category=category,
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the plastic quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, "index.html")
    else:
        return render(request, "plastic.html")

def ewaste(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        cate = request.POST["Category"]
        category = EWASTE[int(cate)-1]
        desc = request.POST["message"]
        feedback = EwasteRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category=category,
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the Ewaste quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, 'index.html')
    else:
        return render(request, "ewaste.html")

def metal(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        cate = request.POST["Category"]
        category = METALS[int(cate)-1]
        desc = request.POST["message"]
        feedback = MetalRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category=category,
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the metal quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, 'index.html')
    else:
        return render(request, "metal.html")

def glass(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        kg = request.POST["Quantity"]
        cate = request.POST["Category"]
        category = GLASS[int(cate)-1]
        desc = request.POST["message"]
        feedback = GlassRequest(fname=fname, 
                                lname=lname, 
                                email=email, 
                                phone=phone, 
                                kg=kg, 
                                category=category,
                                description=desc, 
                                date=datetime.date.today())
        try:
            feedback.save()
            gmail = Gmail()
            send = gmail.run(message=f"Thank you for providing the details of the glass quantity you currently possess. We appreciate your cooperation in sharing this information with us.Your information will assist us in better understanding your requirements and enable us to tailor our services to meet your needs effectively.", 
                            to=str(email), 
                            subject="GreenCycle Contrib")
            if send:
                print("Message sent")
            else:
                print("Couldn't send message")
            return render(request, "index.html")
        except Exception as e:
            print(f"One Error Occured {e}")
            return render(request, "index.html")
    else:
        return render(request, "glass.html")

# Create your views here.
