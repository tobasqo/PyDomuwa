import { GameCategoryApiRoute } from "$lib/api/routes/GameCategoryApiRoute";
import { GameTypeApiRoute } from "$lib/api/routes/GameTypeApiRoute";
import { QnACategoryApiRoute } from "$lib/api/routes/QnACategoryApiRoute";
import { UsersApiRoute } from "$lib/api/routes/UserApiRoute";
import { getHome, type Fetch } from "$lib/api";
import { error, fail, type Cookies } from "@sveltejs/kit";
import { GameTypeSchema, GameTypesSchema } from "$lib/api/types/game_type";
import { QnACategoriesSchema } from "$lib/api/types/qna_category";
import {
	QuestionCreateSchema,
	QuestionSchema,
	QuestionsWithAnswersSchema,
	type QuestionCreate,
} from "$lib/api/types/question";
import { QuestionApiRoute } from "$lib/api/routes/QuestionApiRoute";
import { loginForAccessToken, readCurrentUser, refreshAccessToken } from "./auth";
import { UserCreateSchema, UserSchema, type UserCreate } from "./types/user";

const gameCategoriesRoute = new GameCategoryApiRoute();
const gameTypesRoute = new GameTypeApiRoute();
const qnaCategoriesRoute = new QnACategoryApiRoute();
const questionsRoute = new QuestionApiRoute();
const usersRoute = new UsersApiRoute();

async function getGameType(fetch: Fetch, cookies: Cookies, gameTypeId: number) {
	const response = await gameTypesRoute.getById(fetch, cookies, gameTypeId);
	const responseData = await response.json();
	const gameType = GameTypeSchema.safeParse(responseData);
	if (!gameType.success) {
		throw error(500, "Received malformed game type data from server.");
	}
	return gameType.data;
}

async function getAllGameTypes(fetch: Fetch, cookies: Cookies) {
	const response = await gameTypesRoute.getAll(fetch, cookies);
	const responseData = await response.json();
	const gameTypes = GameTypesSchema.safeParse(responseData);
	if (!gameTypes.success) {
		throw error(500, "Received malformed game types data from server.");
	}
	return gameTypes.data;
}

async function getAllQnACategories(fetch: Fetch, cookies: Cookies) {
	const response = await qnaCategoriesRoute.getAll(fetch, cookies);
	const responseData = await response.json();
	const qnaCategories = QnACategoriesSchema.safeParse(responseData);
	if (!qnaCategories.success) {
		throw error(500, "Received malformed QnA categories data from server.");
	}
	return qnaCategories.data;
}

async function getAllQuestionsForGameType(
	fetch: Fetch,
	cookies: Cookies,
	gameTypeId: number,
) {
	const response = await gameTypesRoute.getAllQuestions(fetch, cookies, gameTypeId);
	const responseData = await response.json();
	const questions = QuestionsWithAnswersSchema.safeParse(responseData);
	if (!questions.success) {
		throw error(500, "Received malformed questions for game type data from server.");
	}
	return questions.data;
}

async function createQuestion(
	fetch: Fetch,
	cookies: Cookies,
	questionData: QuestionCreate,
) {
	const questionCreate = QuestionCreateSchema.safeParse(questionData);
	if (!questionCreate.success) {
		throw questionCreate.error;
	}
	const response = await questionsRoute.create(fetch, cookies, questionCreate.data);
	const responseData = await response.json();
	if (!response.ok) {
		return fail(response.status, { errors: responseData, ...questionData });
	}
	const createdQuestion = QuestionSchema.safeParse(responseData);
	if (!createdQuestion.success) {
		throw error(500, "Received malformed question data from server.");
	}
	return createdQuestion.data;
}

async function createUser(fetch: Fetch, cookies: Cookies, userData: UserCreate) {
	const userCreate = UserCreateSchema.safeParse(userData);
	if (!userCreate.success) {
		return fail(422, { errors: userCreate.error, ...userData });
	}
	const response = await usersRoute.create(fetch, cookies, userCreate.data);
	const responseData = await response.json();
	if (!response.ok) {
		return fail(response.status, { errors: responseData, ...userData });
	}
	const user = UserSchema.safeParse(responseData);
	if (!user.success) {
		throw error(500, "Received malformed user data from server.");
	}
	return user.data;
}

export const apiClient = {
	getHome,

	login: loginForAccessToken,
	refreshAccessToken,
	readCurrentUser,

	createUser,

	getGameType,
	getAllGameTypes,

	getAllQnACategories,

	createQuestion,
	getAllQuestionsForGameType,
};
