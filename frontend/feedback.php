<?php
// Database configuration
define('DB_HOST', 'localhost');  
define('DB_USER', 'root');        
define('DB_PASS', '');            
define('DB_NAME', 'language_app'); 
$conn = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);


if (!$conn) {
    die("Database connection error: " . mysqli_connect_error());
}

$name = $email = $subject = $message = '';
$errors = [];
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $subject = filter_input(INPUT_POST, 'subject', FILTER_SANITIZE_STRING);
    $message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_STRING);

    if (empty($name)) {
        $errors['name'] = 'Name is required';
    }
    
    if (empty($email)) {
        $errors['email'] = 'Email is required';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Invalid email format';
    }
    
    if (empty($subject)) {
        $errors['subject'] = 'Subject is required';
    }
    
    if (empty($message)) {
        $errors['message'] = 'Message is required';
    }

    // If no errors, save to database
    if (empty($errors)) {
        // Prepare the SQL statement
        $stmt = mysqli_prepare($conn, "
            INSERT INTO feedback (name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, NOW())
        ");
        
        // Bind parameters to the SQL query
        mysqli_stmt_bind_param($stmt, "ssss", $name, $email, $subject, $message);

        // Execute the query
        if (mysqli_stmt_execute($stmt)) {
            $success = 'Thank you for your feedback!';
            // Clear form fields
            $name = $email = $subject = $message = '';
        } else {
            $errors[] = "Error: " . mysqli_stmt_error($stmt);
        }

        // Close the statement
        mysqli_stmt_close($stmt);
    }
}

// Close the database connection
mysqli_close($conn);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/style2.css">

    <title>Feedback Form</title>
    <style>
        .feedback-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #2A2F4F;
        }

        input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }

        .error {
            color: #dc3545;
            font-size: 14px;
            margin-top: 5px;
        }

        .success {
            color: #28a745;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            background: #d4edda;
        }

        button {
            background: #2A2F4F;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #917FB3;
        }
    </style>
</head>
<body>

<header>
    <h1>Welcome to the AI English Learning Platform</h1>
    
    <nav>
        <a href="main.html">Home</a>
        <a href="pronunciation.html">Pronunciation Evaluation</a>
        <a href="user_profile.html">User Profile</a>
        <a href="feedback.php">Feedback</a>
        <a href="javascript:void(0);" onclick="logout()">Logout</a>
    </nav>
</header>

    <div class="feedback-container">
        <h2>Send Us Your Feedback</h2>
        
        <?php if ($success): ?>
            <div class="success"><?= $success ?></div>
        <?php endif; ?>

        <?php if (!empty($errors)): ?>
            <div class="error">
                <?php foreach ($errors as $error): ?>
                    <p><?= $error ?></p>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>

        <form method="POST">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" value="<?= htmlspecialchars($name) ?>">
                <?php if (isset($errors['name'])): ?>
                    <span class="error"><?= $errors['name'] ?></span>
                <?php endif; ?>
            </div>

            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" value="<?= htmlspecialchars($email) ?>">
                <?php if (isset($errors['email'])): ?>
                    <span class="error"><?= $errors['email'] ?></span>
                <?php endif; ?>
            </div>

            <div class="form-group">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" value="<?= htmlspecialchars($subject) ?>">
                <?php if (isset($errors['subject'])): ?>
                    <span class="error"><?= $errors['subject'] ?></span>
                <?php endif; ?>
            </div>

            <div class="form-group">
                <label for="message">Message:</label>
                <textarea id="message" name="message" rows="5"><?= htmlspecialchars($message) ?></textarea>
                <?php if (isset($errors['message'])): ?>
                    <span class="error"><?= $errors['message'] ?></span>
                <?php endif; ?>
            </div>

            <button type="submit">Send Feedback</button>
        </form>
    </div>
</body>
</html>