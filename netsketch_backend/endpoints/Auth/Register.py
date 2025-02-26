from rest_framework.views import APIView

#AUTH
class RegisterView(APIView):  
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        imagen =  request.data.get("thumbnail")
        thumbnail_path = create_or_edit_image(imagen, 'create')
        try:
            success, msg = createUser(username=username, email=email, password= password, thumbnail = thumbnail_path)
            return Response({'success': success, 'data':{
                "message": msg
            }}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'success': False, 'data': {"error": e.messages}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'data':  {"error":str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
   
        
    # def changePassword(self, request):
    #     try:
    #         data = json.loads(request.body)
    #         email = data.get('email')
    #         token = data.get('token')
    #         old_password = data.get('old_password')
    #         new_password = data.get('new_password')
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON data."}, status=400)

    #     # Check if all required fields are provided
    #     if not email or not old_password or not new_password:
    #         return JsonResponse({"error": "Email, old password, and new password are required."}, status=400)

    #     # Find the user by email
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return JsonResponse({"error": "User with this email does not exist."}, status=404)

    #     if(user.verification_token != token):
    #         return JsonResponse({"error": "Invalid token."}, status=400)

    #     # Verify the old password
    #     if not check_password(old_password, user.password):
    #         return JsonResponse({"error": "Incorrect old password."}, status=400)

    #     # Update the password
    #     user.password = make_password(new_password)
    #     user.save()

    #     return JsonResponse({"detail": "Password changed successfully."}, status=200)


    # def sendVerificationEmail(self, request):
    #     try:
    #         data = json.loads(request.body)
    #         email = data.get('email')
    #         if not email:
    #             return JsonResponse({"error": "Email is required."}, status=400)
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON data."}, status=400)

    #     # Find the user by email
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return JsonResponse({"error": "User with this email does not exist."}, status=404)

    #     nombre = user.username
        

    #     # Generate a random verification token
    #     verification_token = ''.join(random.choices(string.digits, k=6))
    #     user.verification_token = verification_token
    #     user.save()

    #     mensaje = return_message(nombre, user.verification_token)

    #     msg = MIMEMultipart('alternative')
    #     msg['From'] = "ADMINISTRADOR"
    #     msg['To'] = email
    #     msg['Subject'] = "Account Verification"
    #     msg.attach(MIMEText(mensaje, 'html'))

    #     try:
    #          with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #             server.starttls()
    #             server.login(USER_MAIL, PASSWORD )
    #             server.sendmail(USER_MAIL, email, msg.as_string())
    #             return JsonResponse({"detail": "Token assigned succesfully and email sent"}, status=200)
    #     except Exception as e:
    #         respuesta = {
    #             "msg" : "Error en el login"
    #         }
    #         return HttpResponse(json.dumps(respuesta))
