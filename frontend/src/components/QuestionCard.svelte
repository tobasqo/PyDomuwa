<script lang="ts">
	import type { Question } from "$lib/api/types/question";
	import GameCategoryLabel from "./GameCategoryLabel.svelte"; // TODO: fix relative import

	export let question: Question;
</script>

<li>
	{question.text}
	Autor: {question.author.user.username}
	<GameCategoryLabel gameCategory={question.gameCategory} />
</li>
