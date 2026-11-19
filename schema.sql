-- MySQL Database Setup for Government Scheme Eligibility & Recommendation Assistant
CREATE DATABASE IF NOT EXISTS yojana_sarthi_db;
USE yojana_sarthi_db;

CREATE TABLE IF NOT EXISTS schemes (
    scheme_id INT AUTO_INCREMENT PRIMARY KEY,
    scheme_name VARCHAR(255) NOT NULL,
    category_tag VARCHAR(100) NOT NULL,
    min_age INT DEFAULT 0,
    max_age INT DEFAULT 120,
    max_income DECIMAL(12, 2) DEFAULT 99999999.00,
    allowed_occupations VARCHAR(255) DEFAULT 'All',
    allowed_locations VARCHAR(255) DEFAULT 'All',
    allowed_social_categories VARCHAR(255) DEFAULT 'All',
    benefits TEXT NOT NULL,
    description TEXT NOT NULL,
    official_link VARCHAR(255) DEFAULT 'https://www.myscheme.gov.in/'
);

CREATE TABLE IF NOT EXISTS user_queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150),
    age INT NOT NULL,
    income DECIMAL(12, 2) NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    social_category VARCHAR(50) NOT NULL,
    matched_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Sample Government Schemes
INSERT INTO schemes (scheme_name, category_tag, min_age, max_age, max_income, allowed_occupations, allowed_locations, allowed_social_categories, benefits, description, official_link) VALUES
('PM-KISAN Samman Nidhi', 'Agriculture', 18, 100, 500000, 'Farmer', 'Rural,Semi-Urban,All', 'All', 'Rs. 6,000 per year in 3 equal installments directly into bank accounts.', 'Income support scheme for all landholding farmer families across India.', 'https://pmkisan.gov.in/'),
('Ayushman Bharat PM-JAY', 'Healthcare', 0, 120, 250000, 'All', 'All', 'All', 'Health insurance cover of up to Rs. 5 Lakh per family per year for secondary and tertiary hospitalization.', 'World largest health assurance scheme providing cashless treatment at empanelled hospitals.', 'https://pmjay.gov.in/'),
('PM Mudra Yojana (PMMY)', 'Business & Entrepreneurship', 18, 65, 1500000, 'Self-Employed,Small Business,Unemployed', 'All', 'All', 'Collateral-free micro-credit loans up to Rs. 10 Lakh (Shishu, Kishore, Tarun categories).', 'Provides institutional finance to non-corporate, non-farm small/micro enterprises.', 'https://www.mudra.org.in/'),
('National Means-cum-Merit Scholarship', 'Education', 13, 25, 350000, 'Student', 'All', 'All', 'Scholarship of Rs. 12,000 per annum for meritorious students from economically weaker sections.', 'Financial assistance to arrest drop-out rates and encourage continuation of education.', 'https://scholarships.gov.in/'),
('Post Matric Scholarship for SC/ST/OBC', 'Education', 16, 30, 250000, 'Student', 'All', 'SC,ST,OBC', 'Full tuition fee reimbursement plus monthly maintenance allowance.', 'Supports students belonging to SC, ST, and OBC categories pursuing post-matriculation courses.', 'https://scholarships.gov.in/'),
('PM Awas Yojana (Urban & Gramin)', 'Housing', 18, 75, 600000, 'All', 'Rural,Urban,Semi-Urban,All', 'All', 'Financial assistance / interest subsidy up to Rs. 2.67 Lakh for building a pucca house.', 'Housing for All mission aiming to provide affordable housing to eligible low and middle-income families.', 'https://pmaymis.gov.in/'),
('Atal Pension Yojana (APY)', 'Social Security & Pension', 18, 40, 1000000, 'Unorganized Worker,Self-Employed,Farmer,Worker,All', 'All', 'All', 'Guaranteed minimum monthly pension of Rs. 1,000 to Rs. 5,000 after age 60.', 'Government-backed pension scheme focused on citizens in the unorganized sector.', 'https://npscra.nsdl.co.in/'),
('Indira Gandhi National Old Age Pension', 'Senior Citizen Welfare', 60, 120, 150000, 'Senior Citizen,Retired,Unemployed,All', 'All', 'All', 'Monthly pension support ranging from Rs. 200 to Rs. 500+ (with state top-up) for BPL seniors.', 'Social assistance program providing financial security to elderly citizens living below the poverty line.', 'https://nsap.nic.in/'),
('Stand-Up India Scheme', 'Business & Entrepreneurship', 18, 65, 2500000, 'Self-Employed,Small Business,Unemployed', 'All', 'SC,ST,Women', 'Bank loans between Rs. 10 Lakh and Rs. 1 Crore for setting up a greenfield enterprise.', 'Promotes entrepreneurship among Scheduled Castes, Scheduled Tribes, and Women entrepreneurs.', 'https://www.standupmitra.in/'),
('PM Kaushal Vikas Yojana (PMKVY)', 'Skill Development', 15, 45, 800000, 'Student,Unemployed,Worker', 'All', 'All', 'Free industry-relevant skill training, certification, and placement assistance.', 'Flagship skill certification scheme enabling Indian youth to take up industry-relevant training.', 'https://www.pmkvyofficial.org/'),
('PM SVANidhi Micro-Credit', 'Street Vendors', 18, 65, 300000, 'Self-Employed,Small Business,Worker', 'Urban,Semi-Urban,All', 'All', 'Working capital loan up to Rs. 50,000 with 7% interest subsidy and cashback on digital transactions.', 'Special micro-credit facility for street vendors to resume their livelihoods.', 'https://pmsvanidhi.mohua.gov.in/'),
('Sukanya Samriddhi / Girl Child Education Grant', 'Women & Child Welfare', 0, 18, 800000, 'Student,All', 'All', 'All', 'High-interest tax-free savings (8.2%) and education maturity benefits for girl child.', 'Small deposit scheme under Beti Bachao Beti Padhao to secure the future of the girl child.', 'https://www.india.gov.in/');
