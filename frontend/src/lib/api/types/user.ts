import { z } from "zod";

const MIN_USERNAME_LEN = 4;
const MAX_USERNAME_LEN = 32;
const MIN_PASSWORD_LEN = 8;
const MAX_PASSWORD_LEN = 40;

export const UserCreateSchema = z.object({
	username: z.string().min(MIN_USERNAME_LEN).max(MAX_USERNAME_LEN),
	isStaff: z.boolean().default(false),
	password: z.string().min(MIN_PASSWORD_LEN).max(MAX_PASSWORD_LEN),
});
export type UserCreate = z.infer<typeof UserCreateSchema>;

export const UserUpdateSchema = z.object({
	username: z.string().min(MIN_USERNAME_LEN).max(MAX_USERNAME_LEN).optional(),
	isActive: z.boolean().optional(),
	isStaff: z.boolean().optional(),
	password: z.string().min(MIN_PASSWORD_LEN).max(MAX_PASSWORD_LEN).optional(),
});
export type UserUpdate = z.infer<typeof UserUpdateSchema>;

export const UserSchema = z.object({
	id: z.number().min(1),
	username: z.string().min(MIN_USERNAME_LEN).max(MAX_USERNAME_LEN),
	isActive: z.boolean(),
	isStaff: z.boolean(),
});
export type User = z.infer<typeof UserSchema>;
