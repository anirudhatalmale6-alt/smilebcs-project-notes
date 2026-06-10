<?php
/*
 * Kira Call Webhook - Receives Retell post-call data
 * Sends email summary and logs calls
 */

define('NOTIFY_EMAIL', 'brendan@smileprinting.co.uk');
define('FROM_EMAIL', 'kira@smilecreative.agency');
define('LOG_FILE', __DIR__ . '/call-log.json');
define('LOG_PASSWORD', 'KiraLog2026!');

// Handle GET request - show call log dashboard
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_GET['log'])) {
        session_start();
        if (isset($_POST['log_password']) && $_POST['log_password'] === LOG_PASSWORD) {
            $_SESSION['kira_log_auth'] = true;
        }
        if (empty($_SESSION['kira_log_auth'])) {
            show_login();
            exit;
        }
        show_log();
        exit;
    }
    echo json_encode(['status' => 'ok', 'message' => 'Kira webhook endpoint active']);
    exit;
}

// Handle POST - incoming webhook from Retell
header('Content-Type: application/json');

$raw = file_get_contents('php://input');
$data = json_decode($raw, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

// Extract call data from Retell webhook payload
$call_id = $data['call_id'] ?? $data['id'] ?? 'unknown';
$call_type = $data['call_type'] ?? 'unknown';
$from_number = $data['from_number'] ?? $data['caller_number'] ?? 'Unknown';
$to_number = $data['to_number'] ?? $data['callee_number'] ?? '';
$duration_ms = $data['end_timestamp'] ?? 0;
$start_ms = $data['start_timestamp'] ?? 0;
$duration_secs = ($duration_ms && $start_ms) ? round(($duration_ms - $start_ms) / 1000) : 0;
$status = $data['call_status'] ?? $data['status'] ?? 'completed';
$disconnection = $data['disconnection_reason'] ?? '';

// Get transcript
$transcript = '';
$transcript_obj = $data['transcript_object'] ?? $data['transcript'] ?? [];
if (is_array($transcript_obj)) {
    foreach ($transcript_obj as $turn) {
        $role = $turn['role'] ?? 'unknown';
        $content = $turn['content'] ?? '';
        $label = ($role === 'agent') ? 'Kira' : 'Caller';
        $transcript .= "$label: $content\n";
    }
} elseif (is_string($transcript_obj)) {
    $transcript = $transcript_obj;
}
if (!$transcript) {
    $transcript = $data['transcript'] ?? 'No transcript available';
}

// Get call summary/analysis if available
$summary = $data['call_analysis'] ?? $data['summary'] ?? [];
$caller_name = '';
$reason = '';
if (is_array($summary)) {
    $caller_name = $summary['caller_name'] ?? $summary['name'] ?? '';
    $reason = $summary['call_reason'] ?? $summary['reason'] ?? $summary['summary'] ?? '';
    if (is_array($reason)) $reason = json_encode($reason);
}

// Format duration
$dur_min = floor($duration_secs / 60);
$dur_sec = $duration_secs % 60;
$duration_fmt = $dur_min . ':' . str_pad($dur_sec, 2, '0', STR_PAD_LEFT);

$timestamp = date('Y-m-d H:i:s');
$date_nice = date('l j F Y, g:ia');

// Log the call
$log = [];
if (file_exists(LOG_FILE)) {
    $log = json_decode(file_get_contents(LOG_FILE), true) ?: [];
}
$entry = [
    'call_id' => $call_id,
    'timestamp' => $timestamp,
    'from' => $from_number,
    'to' => $to_number,
    'duration' => $duration_fmt,
    'duration_secs' => $duration_secs,
    'status' => $status,
    'caller_name' => $caller_name,
    'reason' => $reason,
    'transcript' => $transcript,
    'disconnection' => $disconnection,
    'follow_up' => '',
];
array_unshift($log, $entry);
file_put_contents(LOG_FILE, json_encode($log, JSON_PRETTY_PRINT));

// Send email notification
$subject = "Kira Call: " . ($caller_name ?: $from_number) . " ($duration_fmt)";

$body = "
<html><body style='font-family:Arial,sans-serif;color:#333;max-width:600px;margin:0 auto'>
<div style='background:#0B0652;color:#fff;padding:20px 24px;'>
    <h2 style='margin:0;font-size:18px'>Kira - New Call Received</h2>
    <p style='margin:4px 0 0;color:rgba(255,255,255,0.7);font-size:13px'>$date_nice</p>
</div>
<div style='padding:20px 24px;border:1px solid #eee;border-top:none'>
    <table style='width:100%;border-collapse:collapse;font-size:14px'>
        <tr><td style='padding:8px 0;color:#888;width:120px'>Caller</td><td style='padding:8px 0;font-weight:bold'>" . ($caller_name ?: 'Not captured') . "</td></tr>
        <tr><td style='padding:8px 0;color:#888'>Phone</td><td style='padding:8px 0'>$from_number</td></tr>
        <tr><td style='padding:8px 0;color:#888'>Duration</td><td style='padding:8px 0'>$duration_fmt</td></tr>
        <tr><td style='padding:8px 0;color:#888'>Status</td><td style='padding:8px 0'>$status</td></tr>
    </table>
    " . ($reason ? "<div style='margin:16px 0;padding:12px 16px;background:#f5f5f5;border-left:3px solid #0B0652'><strong>Reason:</strong> $reason</div>" : "") . "
    <h3 style='margin:20px 0 8px;font-size:14px;color:#0B0652'>Transcript</h3>
    <div style='background:#f9f9f9;padding:12px 16px;font-size:13px;line-height:1.6;white-space:pre-wrap;border:1px solid #eee'>$transcript</div>
    <p style='margin:20px 0 0;font-size:12px;color:#999'>
        <a href='https://smilecreative.agency/kira/kira-webhook.php?log=1' style='color:#0B0652'>View Call Log</a> |
        Call ID: $call_id
    </p>
</div>
</body></html>";

$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=UTF-8\r\n";
$headers .= "From: Kira <" . FROM_EMAIL . ">\r\n";
$headers .= "Reply-To: " . FROM_EMAIL . "\r\n";

$mail_sent = mail(NOTIFY_EMAIL, $subject, $body, $headers);

echo json_encode([
    'status' => 'ok',
    'logged' => true,
    'emailed' => $mail_sent,
    'call_id' => $call_id,
]);

// ── DASHBOARD FUNCTIONS ──

function show_login() {
?><!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kira Call Log</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#0B0652;display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#fff;padding:2rem;border-radius:8px;width:320px}h1{font-size:1.1rem;margin-bottom:1rem;color:#0B0652}
input{width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:4px;margin-bottom:0.8rem;font-size:14px}
button{width:100%;padding:0.6rem;background:#0B0652;color:#fff;border:none;border-radius:4px;font-size:14px;cursor:pointer}</style></head>
<body><form class="box" method="POST"><h1>Kira Call Log</h1><input type="password" name="log_password" placeholder="Password"><button>Enter</button></form></body></html>
<?php }

function show_log() {
    $log = [];
    if (file_exists(LOG_FILE)) $log = json_decode(file_get_contents(LOG_FILE), true) ?: [];
?><!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kira Call Log</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#f5f5f5;color:#333}
.header{background:#0B0652;color:#fff;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:1.1rem}.header span{color:rgba(255,255,255,0.6);font-size:0.85rem}
.container{max-width:900px;margin:1.5rem auto;padding:0 1rem}
.card{background:#fff;border:1px solid #e5e5e5;margin-bottom:0.8rem;padding:1rem 1.2rem}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem}
.card-header h3{font-size:0.95rem;color:#0B0652}.card-meta{color:#888;font-size:0.8rem}
.card-details{display:flex;gap:1.5rem;font-size:0.85rem;color:#555;margin-bottom:0.6rem}
.card-reason{background:#f9f9f9;padding:0.5rem 0.8rem;font-size:0.85rem;border-left:3px solid #0B0652;margin-bottom:0.6rem}
.transcript-toggle{background:none;border:1px solid #ddd;padding:0.3rem 0.8rem;font-size:0.75rem;cursor:pointer;color:#0B0652}
.transcript{display:none;background:#f9f9f9;padding:0.8rem;font-size:0.8rem;line-height:1.6;white-space:pre-wrap;margin-top:0.5rem;max-height:300px;overflow-y:auto}
.transcript.open{display:block}
.empty{text-align:center;padding:3rem;color:#888}
</style></head><body>
<div class="header"><h1>Kira Call Log</h1><span><?php echo count($log); ?> calls</span></div>
<div class="container">
<?php if (empty($log)): ?>
<div class="empty">No calls logged yet</div>
<?php else: foreach ($log as $i => $c): ?>
<div class="card">
    <div class="card-header">
        <h3><?php echo htmlspecialchars($c['caller_name'] ?: $c['from']); ?></h3>
        <span class="card-meta"><?php echo htmlspecialchars($c['timestamp']); ?></span>
    </div>
    <div class="card-details">
        <span>Phone: <?php echo htmlspecialchars($c['from']); ?></span>
        <span>Duration: <?php echo htmlspecialchars($c['duration']); ?></span>
        <span>Status: <?php echo htmlspecialchars($c['status']); ?></span>
    </div>
    <?php if ($c['reason']): ?><div class="card-reason"><?php echo htmlspecialchars($c['reason']); ?></div><?php endif; ?>
    <button class="transcript-toggle" onclick="this.nextElementSibling.classList.toggle('open');this.textContent=this.nextElementSibling.classList.contains('open')?'Hide Transcript':'Show Transcript'">Show Transcript</button>
    <div class="transcript"><?php echo htmlspecialchars($c['transcript']); ?></div>
</div>
<?php endforeach; endif; ?>
</div></body></html>
<?php }
