<?php
header('Content-Type: application/json; charset=UTF-8');

// Only allow POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Methode nicht erlaubt.']);
    exit;
}

// Collect & sanitize inputs
$name    = htmlspecialchars(trim($_POST['name']    ?? ''), ENT_QUOTES, 'UTF-8');
$email   = trim($_POST['email']   ?? '');
$plan    = htmlspecialchars(trim($_POST['plan']    ?? 'Kein Modell gewählt'), ENT_QUOTES, 'UTF-8');
$message = htmlspecialchars(trim($_POST['message'] ?? ''), ENT_QUOTES, 'UTF-8');

// Validate required fields
if (empty($name) || empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Bitte Name und eine gültige E-Mail-Adresse angeben.']);
    exit;
}

$email = filter_var($email, FILTER_SANITIZE_EMAIL);

// Build email
$to      = 'hookvisuals@gmail.com';
$subject = '=?UTF-8?B?' . base64_encode("Neue Anfrage: $name — Hook Visuals") . '?=';

$body  = "Neue Kontaktanfrage über die Hook Visuals Website\n";
$body .= str_repeat('─', 48) . "\n\n";
$body .= "Hotel / Name:     $name\n";
$body .= "E-Mail:           $email\n";
$body .= "Gewünschtes Abo:  $plan\n\n";
$body .= "Nachricht:\n$message\n\n";
$body .= str_repeat('─', 48) . "\n";
$body .= "Gesendet via hookvisuals.com\n";

$headers  = "From: Hook Visuals Website <noreply@hookvisuals.com>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

// Send
if (mail($to, $subject, $body, $headers)) {
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'E-Mail konnte nicht gesendet werden. Bitte versuche es erneut oder schreib uns direkt an hookvisuals@gmail.com.']);
}
