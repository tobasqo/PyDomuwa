import { z } from "zod";
import { PlayerSchema } from "$lib/api/types/player";
import { GameTypeSchema } from "$lib/api/types/game_type";
import { QnaCategorySchema } from "$lib/api/types/qna_category";
import { AnswerSchema } from "$lib/api/types/answer";

export const QuestionCreateSchema = z.object({
	text: z.string(),
	gameTypeId: z.number().min(1),
	gameCategoryId: z.number().min(1),
});
export type QuestionCreate = z.infer<typeof QuestionCreateSchema>;

export const QuestionUpdateSchema = z.object({
	text: z.string().optional(),
	excluded: z.boolean().optional(),
	gameTypeId: z.number().min(1).optional(),
	gameCategoryId: z.number().min(1).optional(),
});
export type QuestionUpdate = z.infer<typeof QuestionUpdateSchema>;

export const QuestionSchema = z.object({
	id: z.number().min(1),
	text: z.string(),
	excluded: z.boolean(),
	deleted: z.boolean(),
	author: PlayerSchema,
	gameType: GameTypeSchema,
	gameCategory: QnaCategorySchema,
	prevVersionId: z.number().min(1).optional(),
});
export type Question = z.infer<typeof QuestionSchema>;

export const QuestionWithAnswersSchema = QuestionSchema.merge(
	z.object({
		answers: z.array(AnswerSchema),
	}),
);
export type QuestionWithAnswers = z.infer<typeof QuestionWithAnswersSchema>;
