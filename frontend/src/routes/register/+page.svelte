<script lang="ts">
	const { form } = $props();
	console.log("register form errors:", form);
</script>

<main class="bg-skyblue mt-6">
	<div
		class="flex flex-col items-center justify-center align-middle px-6 mx-auto h-full">
		<div
			class="w-full bg-orange rounded-lg shadow sm:max-w-md">
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
				<h1
					class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
					Zarejestruj się
				</h1>

				{#if form}
					<div class="space-y-0">
						{#each Object.entries(form.details) as [field, fieldError]}
							<div class="bg-rose-500 text-white p-2 rounded-lg shadow-lg">
								<h4 class="font-bold">{field}</h4>
								<p class="text-sm">{fieldError}</p>
							</div>
						{/each}
					</div>
				{/if}

				<form class="space-y-4 md:space-y-6" action="/register" method="post">
					<div>
						<label for="username"
									 class="block mb-2 text-sm font-medium text-gray-900">
							Nazwa użytkownika
						</label>
						<input type="text" name="username" id="username"
									 class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
									 placeholder="Mietek" required />
					</div>
					<div>
						<label for="password"
									 class="block mb-2 text-sm font-medium text-gray-900">Hasło</label>
						<input type="password" name="password" id="password" placeholder="••••••••"
									 class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
									 required>
					</div>
					<button type="submit"
									class="w-full text-white bg-lilac hover:bg-dark hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center shadow-lg">
						Zarejestruj się
					</button>
				</form>
			</div>
		</div>
	</div>
</main>
