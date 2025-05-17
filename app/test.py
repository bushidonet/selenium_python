import logging
import os
from time import sleep
from flask import Flask, jsonify
from flasgger import Swagger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
swagger = Swagger(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SELENIUM_REMOTE_URL = os.getenv('SELENIUM_REMOTE_URL', 'http://selenium_chrome:4444/wd/hub')

def create_browser():
    logging.info("Configurando opciones de Chrome")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')  # Tamaño para headless

    logging.info(f"Creando navegador remoto en {SELENIUM_REMOTE_URL}")
    browser = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL,
        options=options
    )
    logging.info("Navegador remoto creado")
    return browser

def ScrollPage(browser, element):
    logging.info("Haciendo scroll al elemento")
    browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", element)
    sleep(2)

def safe_click(browser, by, selector):
    logging.info(f"Esperando que el elemento ({by}, {selector}) sea clickeable")
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((by, selector)))
    logging.info("Scroll hacia el elemento antes de hacer clic")
    browser.execute_script("arguments[0].scrollIntoView(true);", element)
    sleep(1)
    try:
        logging.info(f"Intentando clic normal en elemento ({by}, {selector})")
        element.click()
        logging.info("Clic normal exitoso")
    except Exception as ex:
        logging.warning(f"Clic normal falló, intentando clic con JS en ({by}, {selector}): {ex}")
        browser.execute_script("arguments[0].click();", element)
        logging.info("Clic con JS exitoso")

@app.route('/run_test', methods=['GET'])
def run_test():
    """
    Ejecuta el test Selenium y retorna resultado
    ---
    responses:
      200:
        description: Test ejecutado exitosamente
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    browser = None
    try:
        logging.info('Iniciando navegador remoto Chrome')
        browser = create_browser()

        url = 'https://www.qa-practice.com/elements/button/simple'
        logging.info(f"Abriendo URL: {url}")
        browser.get(url)

        # Espera explícita para botón antes de clic
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'submit-id-submit')))
        safe_click(browser, By.ID, 'submit-id-submit')

        logging.info('Test finalizado correctamente')
        return jsonify({"message": "Test Selenium ejecutado exitosamente"}), 200

    except Exception as e:
        logging.error(f"Error en Selenium: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    finally:
        if browser:
            browser.quit()
            logging.info('Navegador cerrado correctamente')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
