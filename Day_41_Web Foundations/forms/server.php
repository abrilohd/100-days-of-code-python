<?php
/*
 * PHP Intro / Backend Demo
 * Location: forms/server.php
 * Quick features demonstrated:
 *  - Serving an HTML form (GET)
 *  - Handling form POSTs and file uploads
 *  - Returning JSON when requested (query ?action=json or Accept: application/json)
 *  - Reading raw JSON request bodies
 *  - Simple cookies and session usage
 *
 * To test locally using PHP built-in server:
 * 1) Open a terminal
 * 2) cd to the Day 41 folder, e.g.:
 *    cd "c:/100 days of python code/Web Foundation Day 41"
 * 3) Start server:
 *    php -S localhost:8000
 * 4) Open the form at:
 *    http://localhost:8000/forms/input.html
 *  OR open this file directly:
 *    http://localhost:8000/forms/server.php
 */

declare(strict_types=1);

// Basic helpers
function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

// Determine request method and JSON preference
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$wantJson = (isset($_GET['action']) && $_GET['action'] === 'json')
				 || (strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false)
				 || (isset($_GET['format']) && $_GET['format'] === 'json');

// If JSON requested, return a small JSON API demonstration
if ($wantJson) {
		header('Content-Type: application/json; charset=utf-8');
		$result = ['ok' => true, 'method' => $method, 'note' => 'This is a simple JSON endpoint from server.php'];
		if ($method === 'POST') {
				$body = file_get_contents('php://input');
				$decoded = json_decode($body, true);
				$result['received_raw'] = $body;
				$result['received_json'] = $decoded ?? null;
		}
		echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
		exit;
}

// Start session to demonstrate session usage
session_start();
if (! isset($_SESSION['visits'])) { $_SESSION['visits'] = 0; }
$_SESSION['visits']++;

// Process POST form submissions
$flash = [];
if ($method === 'POST') {
		// Simple sanitization / extraction
		$username = trim((string)($_POST['username'] ?? ''));
		$iname    = trim((string)($_POST['iname'] ?? ''));

		// Example: set a cookie for username (expires in 1 hour)
		if ($username !== '') {
				setcookie('demo_username', $username, time() + 3600, '/');
				$flash[] = "Stored cookie demo_username={$username}";
		}

		// File upload handling (input name="upload")
		if (!empty($_FILES['upload']['name'])) {
				$uploadsDir = __DIR__ . DIRECTORY_SEPARATOR . 'uploads';
				if (!is_dir($uploadsDir)) {
						mkdir($uploadsDir, 0755, true);
				}
				$fileTmp  = $_FILES['upload']['tmp_name'];
				$fileName = basename($_FILES['upload']['name']);
				$target   = $uploadsDir . DIRECTORY_SEPARATOR . $fileName;
				if (is_uploaded_file($fileTmp) && move_uploaded_file($fileTmp, $target)) {
						$flash[] = "Uploaded file saved to uploads/{$fileName}";
				} else {
						$flash[] = 'File upload failed or no file provided.';
				}
		}

		// Demonstrate response after POST: show received values (but never echo plain passwords)
		$flash[] = 'Received form fields: username length=' . strlen($username) . ', iname=' . h($iname);
}

// Render a small HTML page illustrating usage
?><!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1">
	<title>PHP Backend Intro — server.php</title>
	<style>body{font-family:Arial,Helvetica,sans-serif;margin:20px;padding:0;background:#f7f7f7}main{max-width:820px;background:#fff;padding:18px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.06)}label{display:block;margin:8px 0 4px}input,button{padding:8px;margin-bottom:8px;width:100%;max-width:420px}pre{background:#111;color:#fff;padding:12px;border-radius:6px;overflow:auto}</style>
</head>
<body>
<main>
	<h1>PHP Backend Intro — server.php</h1>
	<p>This file demonstrates basic backend tasks with plain PHP: handling GET/POST, file uploads, JSON endpoints, cookies, and sessions.</p>

	<h2>Try the HTML form (POST)</h2>
	<form method="post" enctype="multipart/form-data" action="<?php echo h($_SERVER['PHP_SELF']); ?>">
		<label for="username">Username</label>
		<input id="username" name="username" placeholder="username">

		<label for="password">Password (demo only)</label>
		<input id="password" type="password" name="password" placeholder="password">

		<label for="iname">Input name</label>
		<input id="iname" name="iname" placeholder="some value">

		<label for="upload">Upload a small file</label>
		<input id="upload" name="upload" type="file">

		<button type="submit">Submit form</button>
	</form>

	<h2>API / JSON examples</h2>
	<ul>
		<li>Request JSON view: <a href="?action=json">?action=json</a></li>
		<li>Fetch JSON via JavaScript (example):</li>
	</ul>
	<pre id="jsdemo">Running demo…</pre>

	<h2>Server-side info</h2>
	<p>Session visits: <?php echo (int)$_SESSION['visits']; ?></p>
	<?php if (!empty($flash)): ?>
		<h3>Messages</h3>
		<ul>
		<?php foreach ($flash as $m): ?>
			<li><?php echo h($m); ?></li>
		<?php endforeach; ?>
		</ul>
	<?php endif; ?>

	<h3>Cookie demo</h3>
	<p>Cookie <code>demo_username</code> value: <?php echo h($_COOKIE['demo_username'] ?? '(not set)'); ?></p>

	<h3>Uploaded files</h3>
	<p>Uploads dir: <code><?php echo h(realpath(__DIR__ . DIRECTORY_SEPARATOR . 'uploads') ?: 'uploads/ (not created)'); ?></code></p>

	<hr>
	<p style="font-size:0.9em;color:#666">Notes: To test JSON POST, use <code>fetch('/forms/server.php?format=json', {method:'POST', body: JSON.stringify({hello:'world'})})</code> or point your REST client to <code>?action=json</code>.</p>
</main>

<script>
// small demo showing fetch to JSON endpoint
fetch('?action=json').then(r=>r.json()).then(d=>{
	document.getElementById('jsdemo').textContent = JSON.stringify(d, null, 2);
}).catch(e=>{ document.getElementById('jsdemo').textContent = 'Could not fetch JSON endpoint: '+e; });
</script>
</body>
</html>

