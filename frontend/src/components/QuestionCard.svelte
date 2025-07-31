<script lang="ts">
	import type { Question } from "$lib/api/types/question";
	import GameCategoryLabel from "./GameCategoryLabel.svelte";  // TODO: fix relative import

	const question: Question = $props();
</script>

<li>
	{question.text}
	Autor: {question.author.user.username}
	<GameCategoryLabel {...question.gameCategory} />
</li>