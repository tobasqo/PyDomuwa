<script lang="ts">
	import { type GameCategory, GameCategoryChoice } from "$lib/api/types/game_category";
	import { type QnACategory, QnACategoryChoice } from "$lib/api/types/qna_category";

	export let gameCategory: GameCategory | QnACategory;

	let labelColor = "";
	switch (gameCategory.name) {
		case GameCategoryChoice.SFW || QnACategoryChoice.SFW:
			labelColor = "game-category-sfw";
			break;
		case GameCategoryChoice.NSFW || QnACategoryChoice.NSFW:
			labelColor = "game-category-nsfw";
			break;
		case GameCategoryChoice.MIXED:
			labelColor = "game-category-mixed";
			break;
    default:
      throw new Error("Unknown game category");
	}

</script>

<div class="label {labelColor}">
	{gameCategory.name}
</div>
