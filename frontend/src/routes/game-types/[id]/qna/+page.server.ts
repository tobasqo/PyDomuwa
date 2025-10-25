import type { Actions } from "./$types";
import { apiClient } from "$lib/api";

export const load = async ({ fetch, params, cookies }) => {
	const gameTypeId = parseInt(params.id!);
	const gameType = await apiClient.gameTypes.getById(fetch, cookies, gameTypeId);
	const questions = await apiClient.gameTypes.getAllQuestions(
		fetch,
		cookies,
		gameTypeId,
	);
	return { gameType, questions: questions };
};

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
