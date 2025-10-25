import type { Actions } from "./$types";
import { apiClient } from "$lib/api";

export const load = async ({ fetch, params, cookies }) => {
	const gameTypeId = parseInt(params.id!);
	const [gameType, qnaCategories, questions] = await Promise.all([
		apiClient.gameTypes.getById(fetch, cookies, gameTypeId),
		apiClient.qnaCategories.getAll(fetch, cookies),
		apiClient.gameTypes.getAllQuestions(fetch, cookies, gameTypeId),
	]);
	return { gameType, qnaCategories, questions };
}

export const actions = {
	default: async ({ fetch, cookies, request }) => {
		const formData = await request.formData();
		const questionData = {
			text: formData.get("text")!.toString(),
			gameTypeId: parseInt(formData.get("game-type")!.toString()),
			gameCategoryId: parseInt(formData.get("game-category")!.toString()),
		};
		const question = await apiClient.questions.create(fetch, cookies, questionData);
		return { question };
	},
} satisfies Actions;
