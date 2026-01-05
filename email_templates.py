
class EmailTemplates:
    
    @staticmethod
    def credentials_template(employee_name, username, password_temp):
      
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f8f9fa;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #4f46e5 0%, #5b21b6 100%);
                    color: #ffffff;
                    padding: 50px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 32px;
                    margin-bottom: 10px;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                }}
                .header p {{
                    font-size: 15px;
                    opacity: 0.95;
                    font-weight: 300;
                }}
                .content {{
                    padding: 40px 35px;
                }}
                .greeting {{
                    font-size: 16px;
                    color: #1f2937;
                    margin-bottom: 25px;
                    line-height: 1.7;
                }}
                .greeting strong {{
                    color: #4f46e5;
                    font-weight: 600;
                }}
                .section {{
                    margin: 30px 0;
                    padding: 25px;
                    background-color: #f3f4f6;
                    border-left: 4px solid #4f46e5;
                    border-radius: 8px;
                }}
                .section-title {{
                    font-size: 13px;
                    color: #374151;
                    font-weight: 700;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                    letter-spacing: 1.2px;
                }}
                .credentials-box {{
                    background-color: #ffffff;
                    padding: 0;
                    border-radius: 6px;
                    margin: 15px 0;
                }}
                .credential-item {{
                    margin: 12px 0;
                    padding: 14px 16px;
                    background-color: #f9fafb;
                    border-radius: 6px;
                    border-left: 3px solid #5b21b6;
                }}
                .credential-item:last-child {{
                    margin-bottom: 0;
                }}
                .credential-label {{
                    font-size: 11px;
                    color: #6b7280;
                    text-transform: uppercase;
                    font-weight: 700;
                    margin-bottom: 6px;
                    letter-spacing: 0.5px;
                }}
                .credential-value {{
                    font-size: 16px;
                    color: #111827;
                    font-family: 'Courier New', monospace;
                    font-weight: 600;
                    word-break: break-all;
                    background-color: #f3f4f6;
                    padding: 10px 12px;
                    border-radius: 4px;
                    letter-spacing: 0.3px;
                }}
                .button-container {{
                    text-align: center;
                    margin: 35px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 40px;
                    background: linear-gradient(135deg, #4f46e5 0%, #5b21b6 100%);
                    color: #ffffff !important;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 15px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
                    cursor: pointer;
                    text-align: center;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
                }}
                .warning {{
                    background-color: #fef3c7;
                    border-left: 4px solid #f59e0b;
                    padding: 18px;
                    border-radius: 6px;
                    margin: 25px 0;
                }}
                .warning-title {{
                    color: #92400e;
                    font-weight: 700;
                    margin-bottom: 10px;
                    font-size: 14px;
                }}
                .warning-text {{
                    color: #78350f;
                    font-size: 14px;
                    line-height: 1.6;
                }}
                .divider {{
                    height: 1px;
                    background-color: #e5e7eb;
                    margin: 25px 0;
                }}
                .footer {{
                    background-color: #f9fafb;
                    padding: 30px 35px;
                    border-top: 1px solid #e5e7eb;
                    text-align: center;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #6b7280;
                    line-height: 1.8;
                    margin: 10px 0;
                }}
                .footer-brand {{
                    font-weight: 700;
                    color: #4f46e5;
                    margin-bottom: 15px;
                }}
                .footer-links {{
                    font-size: 11px;
                    color: #9ca3af;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Bienvenido!</h1>
                    <p>Tu cuenta ha sido creada exitosamente</p>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        Hola <strong>{employee_name}</strong>,
                        <br><br>
                        Te damos la bienvenida a nuestra plataforma. Tu cuenta de usuario ha sido creada correctamente y está lista para usar.
                    </div>
                    
                    <div class="section">
                        <div class="section-title">Tus Credenciales de Acceso</div>
                        <div class="credentials-box">
                            <div class="credential-item">
                                <div class="credential-label">Usuario</div>
                                <div class="credential-value">{username}</div>
                            </div>
                            <div class="credential-item">
                                <div class="credential-label">Contraseña Temporal</div>
                                <div class="credential-value">{password_temp}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="button-container">
                        <a href="http://localhost:4200/login" class="button" target="_blank">Acceder a la Plataforma</a>
                    </div>
                    
                    <div class="warning">
                        <div class="warning-title">Importante: Seguridad de tu Cuenta</div>
                        <div class="warning-text">
                            La contraseña que recibiste es <strong>temporal</strong>. Por tu seguridad, 
                            cambia tu contraseña en tu primer acceso. Usa una contraseña fuerte con 
                            mayúsculas, minúsculas, números y caracteres especiales.
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-brand">GH 360</div>
                    <div class="footer-text">© 2026 Todos los derechos reservados.</div>
                    <div class="footer-text">Este es un correo automático. Por favor, no respondas directamente a este mensaje.</div>
                    <div class="footer-links">Para consultas, contacta con nuestro equipo de soporte.</div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def password_recovery_template(employee_name, password_temp):
     
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f8f9fa;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #4f46e5 0%, #5b21b6 100%);
                    color: #ffffff;
                    padding: 50px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 32px;
                    margin-bottom: 10px;
                    font-weight: 700;
                    letter-spacing: -0.5px;
                }}
                .header p {{
                    font-size: 15px;
                    opacity: 0.95;
                    font-weight: 300;
                }}
                .content {{
                    padding: 40px 35px;
                }}
                .greeting {{
                    font-size: 16px;
                    color: #1f2937;
                    margin-bottom: 25px;
                    line-height: 1.7;
                }}
                .greeting strong {{
                    color: #4f46e5;
                    font-weight: 600;
                }}
                .section {{
                    margin: 30px 0;
                    padding: 25px;
                    background-color: #f3f4f6;
                    border-left: 4px solid #4f46e5;
                    border-radius: 8px;
                }}
                .section-title {{
                    font-size: 13px;
                    color: #374151;
                    font-weight: 700;
                    margin-bottom: 20px;
                    text-transform: uppercase;
                    letter-spacing: 1.2px;
                }}
                .password-box {{
                    background-color: #ffffff;
                    padding: 25px;
                    border-radius: 6px;
                    margin: 15px 0;
                    text-align: center;
                    border: 2px dashed #4f46e5;
                }}
                .password-label {{
                    font-size: 12px;
                    color: #6b7280;
                    text-transform: uppercase;
                    font-weight: 700;
                    margin-bottom: 12px;
                    display: block;
                    letter-spacing: 0.5px;
                }}
                .password-value {{
                    font-size: 22px;
                    color: #4f46e5;
                    font-family: 'Courier New', monospace;
                    font-weight: 700;
                    padding: 15px;
                    background-color: #f9fafb;
                    border-radius: 6px;
                    word-break: break-all;
                    letter-spacing: 0.3px;
                }}
                .button-container {{
                    text-align: center;
                    margin: 35px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 40px;
                    background: linear-gradient(135deg, #4f46e5 0%, #5b21b6 100%);
                    color: #ffffff !important;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 15px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
                    cursor: pointer;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
                }}
                .warning {{
                    background-color: #fef3c7;
                    border-left: 4px solid #f59e0b;
                    padding: 18px;
                    border-radius: 6px;
                    margin: 25px 0;
                }}
                .warning-title {{
                    color: #92400e;
                    font-weight: 700;
                    margin-bottom: 10px;
                    font-size: 14px;
                }}
                .warning-text {{
                    color: #78350f;
                    font-size: 14px;
                    line-height: 1.6;
                }}
                .divider {{
                    height: 1px;
                    background-color: #e5e7eb;
                    margin: 25px 0;
                }}
                .footer {{
                    background-color: #f9fafb;
                    padding: 30px 35px;
                    border-top: 1px solid #e5e7eb;
                    text-align: center;
                }}
                .footer-text {{
                    font-size: 12px;
                    color: #6b7280;
                    line-height: 1.8;
                    margin: 10px 0;
                }}
                .footer-brand {{
                    font-weight: 700;
                    color: #4f46e5;
                    margin-bottom: 15px;
                }}
                .footer-links {{
                    font-size: 11px;
                    color: #9ca3af;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Recuperación de Contraseña</h1>
                    <p>Se ha generado una nueva contraseña temporal para tu cuenta</p>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        Hola <strong>{employee_name}</strong>,
                        <br><br>
                        Se ha generado una nueva contraseña temporal para acceder a tu cuenta. 
                        A continuación encontrarás los detalles para tu acceso.
                    </div>
                    
                    <div class="section">
                        <div class="section-title">Tu Nueva Contraseña Temporal</div>
                        <div class="password-box">
                            <span class="password-label">Contraseña Temporal:</span>
                            <div class="password-value">{password_temp}</div>
                        </div>
                    </div>
                    
                    <div class="button-container">
                        <a href="http://localhost:4200/login" class="button" target="_blank">Acceder a la Plataforma</a>
                    </div>
                    
                    <div class="warning">
                        <div class="warning-title"> Importante: Seguridad de tu Cuenta</div>
                        <div class="warning-text">
                            Esta contraseña es <strong>temporal</strong>. Debes cambiarla en tu próximo acceso 
                            a la plataforma por una nueva y segura que contenga mayúsculas, minúsculas, 
                            números y caracteres especiales.
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="footer-brand">GH 360</div>
                    <div class="footer-text">© 2026 Todos los derechos reservados.</div>
                    <div class="footer-text">Este es un correo automático. Por favor, no respondas directamente a este mensaje.</div>
                    <div class="footer-links">Para consultas, contacta con nuestro equipo de soporte.</div>
                </div>
            </div>
        </body>
        </html>
        """
