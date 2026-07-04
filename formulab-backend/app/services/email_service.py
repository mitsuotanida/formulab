import httpx
from app.config import settings


def _send(to: str, subject: str, html: str) -> bool:
    if not settings.resend_api_key:
        print(f"[EMAIL DISABLED — configure RESEND_API_KEY to send]\nTo: {to}\nSubject: {subject}")
        return True
    try:
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            json={"from": settings.from_email, "to": [to], "subject": subject, "html": html},
            timeout=10,
        )
        if resp.status_code not in (200, 201):
            print(f"[EMAIL ERROR] status={resp.status_code} body={resp.text}")
            return False
        return True
    except Exception as exc:
        print(f"[EMAIL ERROR] {exc}")
        return False


def _base(title: str, body_html: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#0a0f1e;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:40px 16px;">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#0f1729;border-radius:12px;border:1px solid #1e293b;overflow:hidden;">
        <!-- Header -->
        <tr><td style="background:#111827;padding:28px 32px;text-align:center;border-bottom:1px solid #1e293b;">
          <div style="font-size:40px;margin-bottom:8px;">⚡</div>
          <div style="color:#3b82f6;font-size:24px;font-weight:bold;letter-spacing:1px;">FormuLab</div>
          <div style="color:#64748b;font-size:13px;margin-top:4px;">Plataforma de Formulación Matemática · CII 2750</div>
        </td></tr>
        <!-- Body -->
        <tr><td style="padding:32px;">
          {body_html}
        </td></tr>
        <!-- Footer -->
        <tr><td style="padding:20px 32px;text-align:center;border-top:1px solid #1e293b;">
          <p style="color:#334155;font-size:12px;margin:0;">
            Universidad Diego Portales · Ingeniería Industrial y Comercial<br>
            Si no solicitaste esto, simplemente ignora este correo.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_verification_email(to: str, name: str, token: str) -> bool:
    url = f"{settings.frontend_url}/verify-email?token={token}"
    body = f"""
      <h2 style="color:#e2e8f0;margin:0 0 12px;">Hola, {name} 👋</h2>
      <p style="color:#94a3b8;line-height:1.7;margin:0 0 24px;">
        Tu cuenta en FormuLab fue creada exitosamente.<br>
        Confirma tu correo para activarla y comenzar a resolver ejercicios de optimización.
      </p>
      <div style="text-align:center;margin-bottom:28px;">
        <a href="{url}"
           style="display:inline-block;background:#3b82f6;color:#fff;padding:14px 36px;
                  border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;">
          Verificar mi cuenta
        </a>
      </div>
      <p style="color:#475569;font-size:13px;text-align:center;margin:0;">
        Este enlace es válido por <strong style="color:#94a3b8;">24 horas</strong>.
      </p>"""
    return _send(to, "Verifica tu cuenta en FormuLab ⚡", _base("Verifica tu cuenta", body))


def send_reset_email(to: str, name: str, token: str) -> bool:
    url = f"{settings.frontend_url}/reset-password?token={token}"
    body = f"""
      <h2 style="color:#e2e8f0;margin:0 0 12px;">Restablece tu contraseña</h2>
      <p style="color:#94a3b8;line-height:1.7;margin:0 0 24px;">
        Hola {name}, recibimos una solicitud para restablecer la contraseña de tu cuenta FormuLab.<br>
        Haz clic en el botón para crear una nueva contraseña.
      </p>
      <div style="text-align:center;margin-bottom:28px;">
        <a href="{url}"
           style="display:inline-block;background:#3b82f6;color:#fff;padding:14px 36px;
                  border-radius:8px;text-decoration:none;font-weight:bold;font-size:16px;">
          Restablecer contraseña
        </a>
      </div>
      <p style="color:#dc2626;font-size:13px;text-align:center;margin:0;">
        ⚠️ Este enlace expira en <strong>15 minutos</strong> por seguridad.
      </p>"""
    return _send(to, "Restablece tu contraseña en FormuLab", _base("Restablecer contraseña", body))
