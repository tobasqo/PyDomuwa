import { apiClient, getAxiosInstance, handleApiResult } from "$lib/api/index.js";

export const load = async ({ cookies }) => {
	const axiosInstance = await getAxiosInstance(cookies);
	const gameTypesApiResult = await apiClient.gameTypes.getAll(axiosInstance);
	const gameTypes = handleApiResult(gameTypesApiResult);
	const gameCategoriesApiResult = await apiClient.gameCategories.getAll(axiosInstance);
	const gameCategories = handleApiResult(gameCategoriesApiResult);
	const qnaCategoriesApiResult = await apiClient.qnaCategories.getAll(axiosInstance);
	const qnaCategories = handleApiResult(qnaCategoriesApiResult);
	return {
		gameTypes,
		gameCategories,
		qnaCategories,
	};
};
