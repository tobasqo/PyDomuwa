import type { Actions } from "./$types";
import { apiClient } from "$lib/api/client";
import { ZodError } from "zod";
import { fail } from "@sveltejs/kit";

export const load = async ({ fetch, params, cookies }) => {
	const gameTypeId = parseInt(params.id!);
	const [gameType, qnaCategories, questions] = await Promise.all([
		apiClient.getGameType(fetch, cookies, gameTypeId),
		apiClient.getAllQnACategories(fetch, cookies),
		apiClient.getAllQuestionsForGameType(fetch, cookies, gameTypeId),
	]);
	return { gameType, qnaCategories, questions };
};

export const actions = {
	default: async ({ fetch, cookies, request }) => {
		const formData = await request.formData();
		const questionData = {
			text: formData.get("text")!.toString(),
			gameTypeId: parseInt(formData.get("game-type")!.toString()),
			gameCategoryId: parseInt(formData.get("game-category")!.toString()),
		};
		try {
			const question = await apiClient.createQuestion(fetch, cookies, questionData);
			return { question };
		} catch (error) {
			if (error instanceof ZodError) {
				return fail(422, { errors: error.flatten().fieldErrors, ...questionData });
			}
		}
	},
} satisfies Actions;
