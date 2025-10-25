<script lang="ts">
	import GamesList from "$components/GamesList.svelte";
	import { type PageProps } from "./$types";

	const { data }: PageProps = $props();
</script>

<main class="mx-auto justify-center">
	<div class="mx-auto max-w-screen-xl px-4 py-8 lg:px-6 lg:py-16">
		<div class="grid gap-8 lg:grid-cols-2">
			<!-- <GamesList {gameRooms} /> -->
			<GamesList />
			<article class="rounded-xl bg-orange p-6 shadow-xl">
				<h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
					Pytania i odpowiedzi
				</h2>
				<p class="mb-2 text-gray-700">Tu możesz edytować pytania i&nbsp;odpowiedzi</p>
				{#each data.gameTypes as gameType (gameType.id)}
					<div class="flex items-center justify-between">
						<a
							href="/game-types/{gameType.id}/qna"
							class="inline-flex items-center font-medium text-dark hover:text-mint hover:underline"
						>
							{gameType.name}
							<svg
								class="ml-2 h-4 w-4"
								fill="currentColor"
								viewBox="0 0 20 20"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									fill-rule="evenodd"
									d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
									clip-rule="evenodd"
								></path>
							</svg>
						</a>
					</div>
				{/each}
			</article>
			<article class="rounded-xl bg-orange p-6 shadow-xl">
				<h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">Rankingi</h2>
				<p class="mb-2 text-gray-700">Tu będą rankingi per gra i ogólny</p>
				<a
					href="/ranking"
					class="inline-flex items-center font-medium text-dark hover:text-mint hover:underline"
				>
					Idź do rankingów
					<svg
						class="ml-2 h-4 w-4"
						fill="currentColor"
						viewBox="0 0 20 20"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							fill-rule="evenodd"
							d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
							clip-rule="evenodd"
						></path>
					</svg>
				</a>
			</article>
		</div>
	</div>
</main>
