import { apiClient } from "$lib/api/client";
import { isActionFailure, redirect, type Actions } from "@sveltejs/kit";

export const load = async ({ fetch, params, cookies }) => {
    const gameTypeId = parseInt(params.id!);
    const qnaCategories = await apiClient.getAllQnACategories(fetch, cookies);
    return { gameTypeId, qnaCategories };
}

export const actions = {
    default: async ({ fetch, cookies, request, params }) => {
        const formData = await request.formData();
        const questionData = {
            text: formData.get("text")!.toString(),
            gameTypeId: parseInt(params.id!),
            gameCategoryId: parseInt(formData.get("game-category")!.toString()),
        };
        console.log("questionData:", questionData);
        const result = await apiClient.createQuestion(fetch, cookies, questionData);
        console.log("createQuestion result:", result);
        if (isActionFailure(result)) {
            return result;
        }
        throw redirect(303, `/game-types/${params.id}/qna`);
    },
} satisfies Actions;
