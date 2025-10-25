<script lang="ts">
	import type { Question } from "$lib/api/types/question";
	import QuestionCard from "./QuestionCard.svelte";

	export let questions: Question[];
	console.log("QuestionsList received questions:", questions);
</script>

<ul>
	{#each questions as question (question.id)}
		<li>
			<QuestionCard {question} />
		</li>
	{:else}
		<p class="text-xl font-bold text-center mt-6">Nie mam pytań</p>
	{/each}
</ul>
