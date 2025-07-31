<script lang="ts">
	import type { QuestionWithAnswers } from "$lib/api/types/question";
	import QuestionCard from "./QuestionCard.svelte";  // TODO: fix relative imports
	import { GameTypeChoice } from "$lib/api/types/game_type";

	type QuestionsListProps = {
		questions: QuestionWithAnswers[];
		gameType: GameTypeChoice;
	}
	const { questions, gameType }: QuestionsListProps = $props();
</script>

<ul>
	{#if questions }
		{#each questions as question}
			<li>
				<QuestionCard {...question} />
			</li>
		{/each}
	{:else}
		<h2>Obecnie nie ma dodanych żadnych pytań dla {gameType}</h2>
	{/if}
</ul>
