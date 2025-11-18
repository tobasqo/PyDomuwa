import { z } from "zod";
import { error, type Cookies } from "@sveltejs/kit";
import { getHome, type Fetch } from ".";
import { GameCategoryApiRoute } from "./routes/GameCategoryApiRoute";
import { GameTypeApiRoute } from "./routes/GameTypeApiRoute";
import { QnACategoryApiRoute } from "./routes/QnACategoryApiRoute";
import { QuestionApiRoute } from "./routes/QuestionApiRoute";
import { UsersApiRoute } from "./routes/UserApiRoute";
import { UserCreateSchema, UserSchema, type UserCreate, type User } from "./types/user";
import {
	QuestionCreateSchema,
	QuestionSchema,
	QuestionsSchema,
	type QuestionCreate,
	type Question,
	type Questions,
} from "./types/question";
import {
	GameTypeSchema,
	GameTypesSchema,
	type GameType,
	type GameTypes,
} from "./types/game_type";
import { GameCategoriesSchema, type GameCategories } from "./types/game_category";
import { QnACategoriesSchema, type QnACategories } from "./types/qna_category";
import { loginForAccessToken, readCurrentUser, refreshAccessToken } from "./auth";
import { ApiErrorSchema } from "./types/error";

const usersRoute = new UsersApiRoute();
const gameTypesRoute = new GameTypeApiRoute();
const gameCategoriesRoute = new GameCategoryApiRoute();
const qnaCategoriesRoute = new QnACategoryApiRoute();
const questionsRoute = new QuestionApiRoute();

function validateData<T>(
	schema: z.ZodType<T>,
	data: unknown,
	type: "request" | "response" | "error",
) {
	// TODO: make `data` typed
	const validationResult = schema.safeParse(data);
	if (!validationResult.success) {
		console.log(
			`Malformed api ${type} data: ${JSON.stringify(validationResult.error.flatten().fieldErrors)} from ${JSON.stringify(data)}`,
		);
		throw validationResult.error;
	}
	return validationResult.data;
}

const validateRequestData = <T>(schema: z.ZodType<T>, data: unknown) =>
	validateData<T>(schema, data, "request");

// TODO: make a helper for validating error response

// TODO: this probably should throw svelte error when not validated
const validateResponseData = <T>(schema: z.ZodType<T>, data: unknown) => {
	const validationResult = schema.safeParse(data);
	if (!validationResult.success) {
		console.log(
			`Malformed api response data: ${JSON.stringify(validationResult.error.flatten().fieldErrors)} from ${JSON.stringify(data)}`,
		);
		const errorValidationResult = ApiErrorSchema.safeParse(data);
		if (errorValidationResult.success) {
			throw errorValidationResult.error;
		}
		console.error(
			"Response data is not valid and could not be parsed as ApiError either:",
			JSON.stringify(data),
		);
		throw error(500, validationResult.error); // TODO: probably shouild parse error properly
	}
	return validationResult.data;
};

export const apiClient = {
    home: getHome,

    login: loginForAccessToken,
    refreshToken: refreshAccessToken,
    readMe: readCurrentUser,

    createUser: async (fetch: Fetch, cookies: Cookies, model: UserCreate) => {
        validateRequestData(UserCreateSchema, model);
        const responseData = await usersRoute.create(fetch, cookies, model);
        return validateResponseData<User>(UserSchema, responseData);
    },

    createQuestion: async (fetch: Fetch, cookies: Cookies, model: QuestionCreate) => {
        validateRequestData(QuestionCreateSchema, model);
        const responseData = await questionsRoute.create(fetch, cookies, model);
        return validateResponseData<Question>(QuestionSchema, responseData);
    },
    getAllQuestionsForGameType: async (fetch: Fetch, cookies: Cookies, gameTypeId: number) => {
        const responseData = await gameTypesRoute.getAllQuestions(fetch, cookies, gameTypeId);
        return validateResponseData<Questions>(QuestionsSchema, responseData);
    },

    getGameType: async (fetch: Fetch, cookies: Cookies, gameTypeId: number) => {
        const responseData = await gameTypesRoute.getById(fetch, cookies, gameTypeId);
        return validateResponseData<GameType>(GameTypeSchema, responseData);
    },
    getAllGameTypes: async (fetch: Fetch, cookies: Cookies) => {
        const responseData = await gameTypesRoute.getAll(fetch, cookies);
        return validateResponseData<GameTypes>(GameTypesSchema, responseData);
    },

    getAllGameCategories: async (fetch: Fetch, cookies: Cookies) => {
        const responseData = await gameCategoriesRoute.getAll(fetch, cookies);
        return validateResponseData<GameCategories>(GameCategoriesSchema, responseData);
    },

    getAllQnACategories: async (fetch: Fetch, cookies: Cookies) => {
        const responseData = await qnaCategoriesRoute.getAll(fetch, cookies);
        return validateResponseData<QnACategories>(QnACategoriesSchema, responseData);
    },
};
