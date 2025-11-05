<?php
// Inicia la sesión para almacenar mensajes de error o éxito
session_start();

// Función para manejar el almacenamiento de votos en un archivo (como una base de datos simple)
function handle_vote($email, $vote) {
    $votes_filename = 'votes.txt'; // Archivo donde almacenamos los votos
    $stats_filename = 'stats.txt'; // Archivo donde almacenamos las estadísticas de los votos

    if (!file_exists($votes_filename)) {
        file_put_contents($votes_filename, "");
    }
    
    // Verificar si el email ya ha votado
    $votes = file($votes_filename, FILE_IGNORE_NEW_LINES);
    foreach ($votes as $v) {
        list($v_email) = explode(",", $v);
        if ($v_email === $email) {
            return false; // Ya ha votado
        }
    }

    // Si el email no ha votado, registramos el voto
    file_put_contents($votes_filename, $email . "," . $vote . "\n", FILE_APPEND);

    // Actualizamos las estadísticas de votos
    $stats = file($stats_filename, FILE_IGNORE_NEW_LINES);
    $updated = false;
    foreach ($stats as $index => $stat) {
        list($language, $count) = explode(",", $stat);
        if ($language === $vote) {
            $stats[$index] = $language . "," . ($count + 1); // Incrementamos el contador
            $updated = true;
            break;
        }
    }
    if (!$updated) {
        $stats[] = $vote . ",1"; // Si no existía el lenguaje en las estadísticas, lo agregamos
    }
    // Guardamos las estadísticas actualizadas
    file_put_contents($stats_filename, implode("\n", $stats) . "\n");

    return true; // Voto exitoso
}

// Verificar si se envió el formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $vote = $_POST['language'];
    
    // Verificar si el email ya votó
    if (handle_vote($email, $vote)) {
        $_SESSION['message'] = "Gracias por votar. Tu voto ha sido registrado.";
    } else {
        $_SESSION['message'] = "Usted ya votó. No puede votar dos veces.";
    }
}

// Función para mostrar los resultados
function show_results() {
    $stats_filename = 'stats.txt';
    if (file_exists($stats_filename)) {
        $stats = file($stats_filename, FILE_IGNORE_NEW_LINES);
        echo "<h2>Resultados de la Encuesta:</h2>";
        echo "<ul>";
        foreach ($stats as $stat) {
            list($language, $count) = explode(",", $stat);
            echo "<li><strong>$language</strong>: $count votos</li>";
        }
        echo "</ul>";
    } else {
        echo "<p>No hay resultados disponibles.</p>";
    }
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Votación UNCuyo</title>
    <style>
       body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
            text-align: center;
        }

        header {
            background-color: #003366;
            color: white;
            padding: 20px 0;
        }

        header img {
            width: 150px;
        }

        h1 {
            font-size: 24px;
        }

        .form-container {
            margin: 20px auto;
            padding: 20px;
            max-width: 600px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        input[type="email"], select, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .voting-options img {
            max-width: 50px;
            margin-right: 10px;
        }

        .voting-option {
            text-align: left;
            margin-bottom: 15px;
        }

        footer {
            background-color: #003366;
            color: white;
            padding: 10px 0;
            margin-top: 20px;
        }

        .error-message {
            color: red;
        }

        .success-message {
            color: green;
        }
    </style>

    <script>
        // Función para validar el email
        function validateForm() {
            var email = document.getElementById("email").value;
            var language = document.querySelector('input[name="language"]:checked');
            var errorMessages = [];
            
            // Validación de email
            if (email.length < 7) {
                errorMessages.push("El e-mail debe tener al menos 7 caracteres.");
            }
            if (!email.includes('@') || email.startsWith('@') || email.endsWith('@')) {
                errorMessages.push("El e-mail debe contener una '@' válida.");
            }
            if (!email.includes('.') || email.startsWith('.') || email.endsWith('.')) {
                errorMessages.push("El e-mail debe contener un punto ('.') válido.");
            }
            if (/[!#$%^&*(),?":{}|<>]/g.test(email)) {
                errorMessages.push("El e-mail no debe contener caracteres especiales.");
            }
            // Validación de opción seleccionada
            if (!language) {
                errorMessages.push("Debe seleccionar una opción de votación.");
            }

            if (errorMessages.length > 0) {
                // Mostrar errores
                document.getElementById("error-messages").innerHTML = errorMessages.join("<br>");
                return false; // No enviar el formulario
            }

            return true; // Enviar el formulario
        }
    </script>

</head>
<body>

    <!-- Header con logo de la UNCuyo -->
    <header>
        <img src="https://www.uncuyo.edu.ar/assets/imgs/logo_uncu23.png" alt="Logo UNCuyo">
        <h1>Votación sobre Lenguajes de Programación</h1>
    </header>

    <!-- Mensaje de error o éxito -->
    <div id="error-messages" class="error-message">
        <?php
            if (isset($_SESSION['message'])) {
                echo $_SESSION['message'];
                unset($_SESSION['message']);
            }
        ?>
    </div>

    <!-- Formulario -->
    <div class="form-container">
        <form action="index.php" method="POST" onsubmit="return validateForm()">
            <label for="email">Ingresa tu e-mail:</label>
            <input type="email" id="email" name="email" required>

            <h2>¿Cuál es tu lenguaje de programación favorito?</h2>
            
            <div class="voting-options">
                <!-- Opción 1 -->
                <div class="voting-option">
                    <input type="radio" id="python" name="language" value="Python">
                    <label for="python">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" alt="Python Logo">
                        Python
                    </label>
                </div>

                <!-- Opción 2 -->
                <div class="voting-option">
                    <input type="radio" id="javascript" name="language" value="JavaScript">
                    <label for="javascript">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Unofficial_JavaScript_logo_2.svg/330px-Unofficial_JavaScript_logo_2.svg.png" alt="JavaScript Logo">
                        JavaScript
                    </label>
                </div>

                <!-- Opción 3 -->
                <div class="voting-option">
                    <input type="radio" id="java" name="language" value="Java">
                    <label for="java">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/e/eb/Java_get_powered.jpg" alt="Java Logo">
                        Java
                    </label>
                </div>

                <!-- Opción 4 -->
                <div class="voting-option">
                    <input type="radio" id="prolog" name="language" value="Prolog">
                    <label for="prolog">
                        <img src="https://www.swi-prolog.org/icons/swipl.png" alt="Prolog Logo">
                        Prolog
                    </label>
                </div>
            </div>

            <button type="submit">Enviar</button>
        </form>
    </div>

    <!-- Mostrar resultados -->
    <div class="form-container">
        <?php show_results(); ?>
    </div>

    <!-- Footer -->
    <footer>
        <p>&copy; 2025 Universidad Nacional de Cuyo. Todos los derechos reservados.</p>
    </footer>

</body>
</html>
