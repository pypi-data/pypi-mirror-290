
''''
@guest_addresses.route ("/")
async def home (request):
	cookies = request.cookies;
	
	if 'consent' in cookies:
		if cookies ["consent"] == "yes":
			return await sanic_response.file (the_index)
	
	consent_form_HTML = consent_form ({})
	
	return sanic_response.raw (
		consent_form_HTML, 
		content_type = "text/html",
		headers = {}
	)

"'''


def consent_form (packet):
	return f"""
<html>
<head></head>
<body
	style="
		display: flex;
		justify-content: center;
		align-content: center;
		flex-direction: column;
	
		margin: 0;
		padding: 0;
		
		height: 100vh;
		width: 100vw;
		
		overflow-y: scroll;
		
		background: #49F;
	"
>
	<main
		style="
			margin: 0 auto;
			max-width: 10cm;
			height: fit-content;
			
			padding: 1cm;
			border-radius: 1cm;
			
			background: #FFF;
		"
	>
		<header
			style="
				font-size: 1.4em;
				text-align: center;
			"
		>Consent Form</header>
		
		<div style="height: 12px"></div>
		
		<p>For an action with this trinket to be consensual, the party that plays the action must take full responsibility for the action and thus not hold the trinket builders responsible for the action.</p>
		
		<div style="height: 12px"></div>
		
		<p>Once open, it is the responsibility of the consenting party to protect the web browser from interlopers.</p>
		
		<div style="height: 12px"></div>
		
		<p>This trinket requires saving info to browser local storage.</p>
		
		<div style="height: 12px"></div>
		
		<button
			style="
				
			"
		>Consent</button>
	</main>
</body>	
	"""

