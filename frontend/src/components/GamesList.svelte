<script lang="ts">
	export const gameRooms = [];
</script>

<article
	class="p-6 bg-orange rounded-xl shadow-xl">
	<h2
		class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
		Pokoje gier
	</h2>
	<p class="mb-2 text-gray-700">
		Tu będzie lista obecnie rozgrywających się gier. Serwer tego jeszcze nie wspiera
	</p>
	<div class="flex justify-between items-center">
		<a href="/game-rooms/create"
			 class="inline-flex items-center font-medium text-dark hover:underline hover:text-mint">
			Stwórz nową grę
			<svg class="ml-2 w-4 h-4" fill="currentColor" viewBox="0 0 20 20"
					 xmlns="http://www.w3.org/2000/svg">
				<path fill-rule="evenodd"
							d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
							clip-rule="evenodd"></path>
			</svg>
		</a>
	</div>
</article>
