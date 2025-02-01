<script>
	let ip = '192.168.1.72';
	let port = 6455;

	// Predefined colors
	const colors = {
		red: { r: 255, g: 0, b: 0 },
		blue: { r: 0, g: 0, b: 255 },
		green: { r: 0, g: 255, b: 0 },
		clear: { r: 0, g: 0, b: 0 }
	};

	// Function to send LED data
	async function setAllLeds(color) {
		// Generate data for all LEDs
		const ledData = Array.from(
			{ length: 600 },
			(_, i) => `${i}:${color.r},${color.g},${color.b};`
		).join('');

		try {
			const response = await fetch('/api/send-led-data', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ ip, port, data: ledData })
			});

			if (response.ok) {
				console.log('LEDs updated successfully');
			} else {
				console.error('Failed to update LEDs:', response.statusText);
			}
		} catch (error) {
			console.error('Error sending LED data:', error);
		}
	}
</script>

<div>
	<h1>LED Control Panel</h1>

	<div class="button-container">
		<button class="red" on:click={() => setAllLeds(colors.red)}>Red</button>
		<button class="blue" on:click={() => setAllLeds(colors.blue)}>Blue</button>
		<button class="green" on:click={() => setAllLeds(colors.green)}>Green</button>
		<button class="clear" on:click={() => setAllLeds(colors.clear)}>Clear</button>
	</div>
</div>

<style>
	.button-container {
		display: flex;
		gap: 10px;
		margin-top: 20px;
	}

	button {
		padding: 10px 20px;
		font-size: 16px;
		border: none;
		cursor: pointer;
		border-radius: 5px;
		color: white;
	}

	.red {
		background-color: red;
	}

	.blue {
		background-color: blue;
	}

	.green {
		background-color: green;
	}

	.clear {
		background-color: gray;
	}
</style>
