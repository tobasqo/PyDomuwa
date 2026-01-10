export const actions = {
  default: async ({ fetch, cookies, request }) => {
    const formData = await request.formData();
    const questionData = {
      text: formData.get("text")!.toString(),
      gameTypeId: parseInt(formData.get("game-type")!.toString()),
      gameCategoryId: parseInt(formData.get("game-category")!.toString()),
    };
    const question = await apiClient.createQuestion(fetch, cookies, questionData);
    return { ...question };
  },
} satisfies Actions;
