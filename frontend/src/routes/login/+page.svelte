<script lang="ts">
	import type { PageProps } from "../$types";

	const { form }: PageProps = $props();
</script>

<main class="mt-6 bg-skyblue">
	<div
		class="mx-auto flex h-full flex-col items-center justify-center px-6 align-middle"
	>
		<div class="w-full rounded-lg bg-orange shadow sm:max-w-md">
			<div class="space-y-4 p-6 sm:p-8 md:space-y-6">
				<h1
					class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl"
				>
					Zaloguj się
				</h1>

				{#if form}
					<div class="space-y-0">
						<!-- TODO: why details cannot be found? -->
						{#each Object.entries(form.details) as [field, fieldError]}
							<div class="rounded-lg bg-rose-500 p-2 text-white shadow-lg">
								<h4 class="font-bold">{field}</h4>
								<p class="text-sm">{fieldError}</p>
							</div>
						{/each}
					</div>
				{/if}

				<form class="space-y-4 md:space-y-6" action="/login" method="post">
					<div>
						<label for="username" class="mb-2 block text-sm font-medium text-gray-900">
							Nazwa użytkownika
						</label>
						<input
							type="text"
							name="username"
							id="username"
							class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900"
							placeholder="Gucci Boss"
							required
						/>
					</div>
					<div>
						<label for="password" class="mb-2 block text-sm font-medium text-gray-900">
							Hasło
						</label>
						<input
							type="password"
							name="password"
							id="password"
							placeholder="••••••••"
							class="focus:ring-primary-600 focus:border-primary-600 block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900"
							required
						/>
					</div>
					<button
						type="submit"
						class="focus:ring-primary-300 w-full rounded-lg bg-lilac px-5 py-2.5 text-center text-sm font-medium text-white focus:outline-none focus:ring-4"
					>
						Zaloguj się
					</button>
				</form>

				<p class="flex justify-between text-sm font-light text-gray-600">
					<span>Nie masz jeszcze konta?</span>
					<a
						href="/register"
						class="font-medium text-dark hover:text-mint hover:underline"
					>
						Zarejestruj się
					</a>
				</p>
			</div>
		</div>
	</div>
</main>
