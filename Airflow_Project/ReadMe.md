# **Project Documentation**

## **How to Run the Project**

### **Step 1: Set Up Virtual Environment**

1. **Download the Project Files**: After downloading the project files, open a terminal window in the project directory use wsl and enter mnt/the directory letter and so on.

2. **Create a Virtual Environment**: Use the following command to create a virtual environment:
   ```bash
   python3 -m venv airflow_env
   ```

3. **Activate the Virtual Environment**: Once created, activate the virtual environment with the following command:
   ```bash
   source airflow_env\bin\activate
   ```

4. **Install Required Packages**: Install all dependencies listed in `requirements.txt` by running:
   ```bash
    pip3 install -r requirements.txt
   ```
### **Step 2: Run The Project**

5. **Navigate to the Django Project Directory**: Ensure you're in the directory containing `manage.py`.

6. **Create a super user to enter Admin webpage**: Run the following command:
    ```bash
    python3 manage.py createsuperuser
    ```
    You will enter the username then email and password

7. **Start the Django Server**:  Run the following command to start the server:
   ```bash
    python manage.py runserver 8001
   ```

8. **Access the Admin webpage to enter instances**:  Once the server is running, you can interact with it:
    ```ruby
    http://127.0.0.1:8000/admin/
    ```
9. **Start the Django Server for the previous project**:  Run the following command to start the server:
   ```bash
    docker pull alinasser930/my_django_app
   ```
    I uploaded my image I built to dockerhub. So, I don't need to upload both projects and make you create the image. Also, I will provide how to create the image using dockerfile.
    ```bash
    docker build -t my_django_app .
   ```
    This is how you build the docker image using the docker file provided in the repo, but don't use this command
    ```bash
    docker run -d -p 8000:8000 --name my_django_container my_django_app
   ```
   This command will run the container and the project will run properly.
10. **Access the API Endpoint**:  Once the server is running, you can interact with the API using a tool like Postman. The API endpoint for calculations is:
    ```ruby
    http://127.0.0.1:8000/api/
    ```
    And you can enter KPIS, Linker or Assets
    ```ruby
    http://127.0.0.1:8000/api/input/ingester/
    ```
    here you can enter to The API that returns the calculated value to the new Project.
    You can test it using this command:
    ```json
    {
        "asset_id": "1",
        "attribute_id": "1",
        "timestamp": "2022-07-31T23:28:47Z[UTC]",
        "value": "10"
    }
    ```
    The Value should be 60


11. **Start Running Airflow**: 

    Now after setting the environment and intitating the projects you can run
    ```bash
    airflow users create -u admin -f admin -l admin -r Admin -e airflowemail@gmail.com
    ```
    then you enter your password that will be used to enter the Airflow UI

    ```bash
    airflow scheduler
    ```
    run this command in another terminal
    ```bash
    airflow webserver
    ```
    run this command in another terminal

    And you can use Airflow UI
    ```ruby
    http://127.0.0.1:8080/
    ```

    Finally all components are now working you can enjoy using it.


12. **Deactivate Virtual Environment**: deactivate the virtual environment when you are done, like this in the terminal:
    ```bash
    deactivate
    ```

**Ensure you keep the virtual environment activated while running the project and installing any additional dependencies in the future.**



**Enjoy using the project!**