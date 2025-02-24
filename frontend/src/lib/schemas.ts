
import { z } from "zod";

export const submissionSchema = z.object({
    start: z.string()
        .transform((val) => new Date(val))
        .refine((date) => !isNaN(date.getTime()), { message: "Invalid date" })
        .refine((date) => date >= new Date(), { message: "Start date must be in the future" }),
    end: z.string()
        .transform((val) => new Date(val))
        .refine((date) => !isNaN(date.getTime()), { message: "Invalid date" }),
    curriculum_ref: z.string().nonempty(),
    total_costs: z.number().positive(),
    transportation_costs: z.number().positive(),
    parental_info: z.string().nonempty(),
    teachers: z.array(z.string()).length(1),
    students: z.array(z.string()).length(1),
    address: z.object({
        street: z.string().nonempty(),
        city: z.string().nonempty(),
        country: z.string().nonempty(),
        state: z.string().nonempty(),
        zip: z.string().nonempty()
    })
}).refine((schema) => {
    console.log(schema.start, schema.end);
    return schema.start < schema.end;
}, "End must be after start date");

export type SubmissionSchema = typeof submissionSchema;
