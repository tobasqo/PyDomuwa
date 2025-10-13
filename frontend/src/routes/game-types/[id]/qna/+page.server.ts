import type { Actions } from "./$types";
import { error, fail, redirect } from "@sveltejs/kit";
import { getJwtToken } from "$lib/api/auth";
import { apiClient, getAxiosInstance } from "$lib/api";

export const load = async ({ params, cookies }) => {
	const jwtToken = getJwtToken(cookies);
	if (!jwtToken) {
		throw redirect(303, "/login");
	}
	const gameTypeId = parseInt(params.id);
	const axiosInstance = await getAxiosInstance(cookies);
	const gameTypeApiResult = await apiClient.gameTypes.getById(
		axiosInstance,
		gameTypeId,
	);
	if (gameTypeApiResult.error !== null) {
		if (gameTypeApiResult.error.status === 401) {
			throw redirect(303, "/login");
		}
		throw error(gameTypeApiResult.error.status, gameTypeApiResult.error.message);
	}
	const questionsApiResult = await apiClient.gameTypes.getAllQuestions(
		axiosInstance,
		parseInt(params.id),
	);
	if (questionsApiResult.error !== null) {
		if (questionsApiResult.error.status === 401) {
			throw redirect(303, "/login");
		}
		throw error(questionsApiResult.error.status, questionsApiResult.error.message);
	}
	return { gameType: gameTypeApiResult.data, questions: questionsApiResult.data };
};

export const actions = {
	default: async ({ cookies, request }) => {
		const formData = await request.formData();
		console.log(formData);
		const axiosInstance = await getAxiosInstance(cookies);
		const apiResult = await apiClient.questions.create(axiosInstance, {
			text: formData.get("text")!.toString(),
			gameTypeId: parseInt(formData.get("game-type")!.toString()),
			gameCategoryId: parseInt(formData.get("game-category")!.toString()),
		});
		if (apiResult.error !== null) {
			return fail(apiResult.error.status, {
				error: apiResult.error.message,
				details: apiResult.error.details(),
			});
		}
		return { questions: apiResult.data };
	},
} satisfies Actions;
