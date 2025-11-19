import { apiClient } from "$lib/api/client";

export const load = async ({ fetch, params, cookies }) => {
	const gameTypeId = parseInt(params.id!);
	console.log("Loading QnA page for gameTypeId:", gameTypeId);
	const [gameType, questions] = await Promise.all([
		apiClient.getGameType(fetch, cookies, gameTypeId),
		apiClient.getAllQuestionsForGameType(fetch, cookies, gameTypeId),
	]);
	return { gameType, questions };
};
