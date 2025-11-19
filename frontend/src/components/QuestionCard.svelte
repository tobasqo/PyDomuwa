<script lang="ts">
	import type { Question } from "$lib/api/types/question";
	import GameCategoryLabel from "./GameCategoryLabel.svelte"; // TODO: fix relative import

	export let question: Question;
</script>

<div class="justify-center my-2 px-4 py-2">
  <h3 class="text-l font-bold text-gray-900">
    {question.text}
  </h3>
  Autor: {question.author.user.username}
  <GameCategoryLabel gameCategory={question.gameCategory} />
</div>
