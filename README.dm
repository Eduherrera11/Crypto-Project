🚀 Proyecto de Gestión de Inversiones en Criptomonedas / Cryptocurrency Investment Management Project
📄 Descripción del Proyecto / Project Description
ES: El objetivo de este proyecto es desarrollar un programa en Python que se conecte a una base de datos MySQL y proporcione una experiencia interactiva en la terminal para gestionar inversiones en criptomonedas. El programa permitirá al usuario realizar varias operaciones relacionadas con sus inversiones y mostrará información relevante de manera clara y organizada.

EN: The goal of this project is to develop a Python program that connects to a MySQL database and provides an interactive terminal experience for managing cryptocurrency investments. The program will allow users to perform various operations related to their investments and display relevant information in a clear and organized manner.

⚙️ Funcionalidades Requeridas / Required Features
🗄️ Conexión a la Base de Datos MySQL / MySQL Database Connection
ES: Establecer una conexión con una base de datos MySQL.

EN: Establish a connection to a MySQL database.

ES: Asegurar que la base de datos contenga las tablas necesarias para almacenar la información de las inversiones del usuario (fecha de inversión, precio de compra, cantidad comprada, tipo de criptomoneda, etc.).

EN: Ensure that the database contains the necessary tables to store user investment information (investment date, purchase price, amount bought, type of cryptocurrency, etc.).

💻 Interfaz de Usuario en la Terminal / Terminal User Interface
ES: Crear un menú interactivo en la terminal que ofrezca varias opciones al usuario:

EN: Create an interactive terminal menu offering several options to the user:

ES: Agregar una nueva inversión en criptomonedas.

EN: Add a new cryptocurrency investment.

ES: Mostrar el precio actual de una criptomoneda específica.

EN: Show the current price of a specific cryptocurrency.

ES: Mostrar la cantidad total invertida por el usuario en cada criptomoneda.

EN: Show the total amount invested by the user in each cryptocurrency.

ES: Listar todas las criptomonedas compradas por el usuario con sus respectivos detalles (fecha, precio, cantidad).

EN: List all cryptocurrencies bought by the user with respective details (date, price, amount).

ES: Calcular y mostrar cuánto dinero tendría el usuario si vendiera sus criptomonedas a un precio especificado.

EN: Calculate and display how much money the user would have if they sold their cryptocurrencies at a specified price.

ES: Mostrar el rendimiento de las inversiones del usuario tanto con el precio actual como con un precio especificado, expresado en porcentaje.

EN: Show the user's investment performance with both the current price and a specified price, expressed as a percentage.

ES: Calcular el valor deseado de una criptomoneda.

EN: Calculate the desired value of a cryptocurrency.

ES: Poner un target en los precios de las criptomonedas.

EN: Set a target for cryptocurrency prices.

ES: Análisis de Stop Profit.

EN: Stop Profit Analysis.

ES: Análisis de Stop Profit Continuo (ejecutado cada 5 segundos).

EN: Continuous Stop Profit Analysis (executed every 5 seconds).

➕ Agregar Inversiones / Add Investments
ES: Solicitar al usuario la fecha de la inversión, el precio de compra, la cantidad y el tipo de criptomoneda.

EN: Request the user to enter the investment date, purchase price, amount, and type of cryptocurrency.

ES: Guardar esta información en la base de datos.

EN: Save this information in the database.

💰 Mostrar Precio Actual de Criptomonedas / Show Current Cryptocurrency Price
ES: Obtener el precio actual de una criptomoneda específica utilizando una API externa de precios de criptomonedas (por ejemplo, CoinGecko o CoinMarketCap).

EN: Retrieve the current price of a specific cryptocurrency using an external cryptocurrency price API (e.g., CoinGecko or CoinMarketCap).

ES: Mostrar el precio actual en la terminal.

EN: Display the current price in the terminal.

📊 Calcular y Mostrar Inversiones / Calculate and Display Investments
ES: Consultar la base de datos para obtener la cantidad total invertida por el usuario en cada criptomoneda.

EN: Query the database to obtain the total amount invested by the user in each cryptocurrency.

ES: Listar todas las inversiones del usuario con detalles de fecha, precio y cantidad.

EN: List all user investments with details such as date, price, and amount.

📈 Calcular Valor Actual y Rendimiento / Calculate Current Value and Performance
ES: Calcular el valor actual de las inversiones del usuario utilizando el precio actual de las criptomonedas.

EN: Calculate the current value of the user's investments using the current cryptocurrency prices.

ES: Calcular cuánto dinero tendría el usuario si vendiera todas sus criptomonedas a un precio especificado por él.

EN: Calculate how much money the user would have if they sold all their cryptocurrencies at a specified price.

ES: Mostrar el rendimiento de las inversiones del usuario en porcentaje, comparando el precio de compra con el precio actual o el precio especificado.

EN: Display the user's investment performance in percentage, comparing the purchase price with the current or specified price.

🔧 Instalación / Installation
ES: Clona este repositorio:
EN: Clone this repository:

sh
Copiar código
git clone https://github.com/usuario/proyecto-crypto.git
cd proyecto-crypto
ES: Crea y activa un entorno virtual:
EN: Create and activate a virtual environment:

sh
Copiar código
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
ES: Instala las dependencias necesarias:
EN: Install the required dependencies:

sh
Copiar código
pip install -r requirements.txt
ES: Configura la base de datos MySQL y ejecuta el script SQL para crear las tablas necesarias.
EN: Set up the MySQL database and run the SQL script to create the necessary tables.

ES: Ejecuta el programa:
EN: Run the program:

sh
Copiar código
python main.py
📂 Estructura del Proyecto / Project Structure
plaintext
Copiar código
proyecto-crypto/
│
├── src/
│   ├── __init__.py
│   ├── menu.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── mysql_connector.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── authentication.py
│   ├── crypto/
│   │   ├── __init__.py
│   │   ├── investments.py
│   │   └── price_analysis.py
│   └── utils/
│       ├── __init__.py
│       ├── email_service.py
│       └── helpers.py
│
├── requirements.txt
├── .env
└── README.md
📜 Licencia / License
ES: Este proyecto está bajo la licencia MIT.
EN: This project is licensed under the MIT License.

✨ Contribuciones / Contributions
ES: Las contribuciones son bienvenidas. Por favor, sigue las pautas de contribución antes de enviar un pull request.
EN: Contributions are welcome. Please follow the contribution guidelines before submitting a pull request.