  IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='content_ideas' AND xtype='U')
        CREATE TABLE staging.content_ideas ( 
    platform VARCHAR(max),
            idea VARCHAR(max),
            description VARCHAR(max),
            topic VARCHAR(max),
            title VARCHAR(max),
            video_description VARCHAR(max),
            audience_appeal VARCHAR(max),
            outline VARCHAR(max),
            hook VARCHAR(max)
        )

        drop table  staging.content_ideas

INSERT INTO staging.content_ideas (platform, idea, description, topic, title, video_description, audience_appeal, outline, hook)
            VALUES
         ('YouTube', 'Webinar series on Advanced Big Data Engineering Solutions', 'A series of webinars that delve into the complexities of big data engineering. The series would explore various tools and technologies used by data engineers on a daily basis, provide tutorials and walkthroughs, and analyze case studies on the most trending topics in the field.', 'Data Engineering', 'Mastering Modern Data Engineering Methodologies: A Comprehensive Guide to Big Data Solutions', 'In this webinar series, we will take an in-depth look at the modern tools and technologies used in big data engineering. With practical examples, walkthroughs, expert interviews and case studies, we aim to provide you with a robust knowledge of managing data effectively. Perfect for aspiring data engineers and anyone interested in the field!', 'Aspiring data engineers, professionals in the tech industry, students in the field of data science and big data, and anyone curious about how they can harness the power of big data.', '["Introduction to big data engineering and its growing relevance", "In-depth explanation of key terms and tools", "Tutorials and walkthroughs of various big data engineering processes", "Discussion on trending topics in data engineering", "Expert interviews and case studies analysis", "Conclusion, Q&A session"]', 'Want to master modern big data engineering methodologies in-depth? Join our comprehensive guide about the big data technologies that are revolutionizing the tech industry!')
         select * from  staging.content_ideas