# Chat de Asistencia Técnica para Plomeros

Este es un chat en tiempo real diseñado para que plomeros se comuniquen con un agente de asistencia técnica. El objetivo es facilitar la resolución de problemas técnicos y la creación de estimados de trabajo de manera eficiente. La plataforma está construida con **FastAPI** y **WebSockets**, y utiliza **n8n** para procesar la lógica de negocio.

---

### Funcionalidades

* **Chat en Tiempo Real:** Los plomeros pueden enviar mensajes y recibir respuestas del agente de asistencia de forma instantánea.
* **Asistencia Técnica:** El agente puede proporcionar soluciones a problemas comunes, guiar en la instalación de equipos o diagnosticar fallas.
* **Creación de Estimados:** El agente puede generar estimados de costos en respuesta a las consultas de los plomeros.
* **Integración con n8n:** Cada mensaje enviado en el chat es procesado por un webhook de n8n, lo que permite una integración fluida con otros servicios (por ejemplo, guardar el historial del chat en una base de datos, enviar notificaciones o crear registros en un CRM).

---

### Arquitectura

La aplicación se compone de tres partes principales:

1.  **Servidor FastAPI (Backend):**
    * Gestiona las conexiones de **WebSockets**.
    * Recibe los mensajes de los plomeros.
    * Envía cada mensaje a un **webhook de n8n**.
    * Reenvía los mensajes a todos los clientes conectados, manteniendo el flujo del chat en tiempo real.

2.  **Cliente (Frontend):**
    * Una interfaz de usuario web simple que se conecta al servidor de FastAPI a través de un WebSocket.
    * Permite a los plomeros escribir y ver los mensajes en la conversación.

3.  **n8n (Lógica de Negocio):**
    * Recibe los mensajes a través de un webhook.
    * Aquí es donde se define la lógica de negocio:
        * Guardar el mensaje en una base de datos (por ejemplo, PostgreSQL, MongoDB).
        * Enviar una notificación al agente de asistencia técnica.
        * Automatizar la creación de un estimado de trabajo basado en la conversación.

![Diagrama de Arquitectura](https://i.imgur.com/your-image-url.png)
_Nota: Puedes reemplazar la URL de la imagen con un diagrama de tu arquitectura si lo deseas._

---

### Requisitos del Sistema

* Python 3.7+
* pip
* n8n (instalado localmente o en un servidor)

---

### Instalación y Ejecución

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
    cd nombre-del-repo
    ```

2.  **Instalar dependencias de Python:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar el Webhook de n8n:**
    * Crea un nuevo workflow en n8n con un nodo de **Webhook**.
    * Copia la URL del webhook.
    * Asegúrate de que la URL del webhook esté configurada en las variables de entorno o en el archivo de configuración del proyecto.

4.  **Ejecutar el servidor FastAPI:**

    ```bash
    uvicorn main:app --reload
    ```

    El servidor se ejecutará en `http://127.0.0.1:8000`.

---

### Uso

* Accede a la URL del servidor en tu navegador para interactuar con la interfaz del chat.
* La comunicación con el agente se manejará a través del backend de FastAPI, que a su vez se comunicará con n8n para cualquier proceso de negocio.

---

### Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.

---

### Licencia

Este proyecto está bajo la Licencia [MIT](https://opensource.org/licenses/MIT).