<?php
use App\Models\Question;
use App\Models\Subcategory;
use App\Models\User;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

require __DIR__ . '/vendor/autoload.php';
$app = require __DIR__ . '/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$user = User::first();

// Wipe placeholder sample/extra questions we seeded
DB::table('questions')->where('stem', 'like', '%Which option is correct?%')->delete();
DB::table('questions')->where('explanation', 'like', '%Local Docker sample%')->delete();
DB::table('questions')->where('explanation', 'like', '%Local sample for Docker%')->delete();

$bank = [
  'Philippine Constitution' => [
    ['The supreme law of the Philippines is the:', ['Constitution', 'Civil Code', 'Penal Code', 'Local Government Code'], 0],
    ['The Philippines is a democratic and republican State. Sovereignty resides in the:', ['People', 'President', 'Congress', 'Supreme Court'], 0],
    ['The term of the President of the Philippines is:', ['6 years', '4 years', '5 years', '3 years'], 0],
    ['Which branch has the power to make laws?', ['Legislative', 'Executive', 'Judiciary', 'Constitutional Commissions'], 0],
    ['The Bill of Rights is found mainly in:', ['Article III', 'Article II', 'Article VI', 'Article VII'], 0],
  ],
  'Code of Conduct and Ethical Standards (R.A. 6713)' => [
    ['R.A. 6713 is also known as the:', ['Code of Conduct and Ethical Standards for Public Officials and Employees', 'Anti-Graft and Corrupt Practices Act', 'Civil Service Law', 'Government Procurement Act'], 0],
    ['Public officials must prioritize:', ['Public interest over personal interest', 'Personal interest over public interest', 'Party loyalty', 'Media coverage'], 0],
    ['Disclosure of conflict of interest is an example of:', ['Transparency and accountability', 'Political neutrality only', 'Simple courtesy', 'Optional practice'], 0],
  ],
  'Peace and Human Rights Issues and Concepts' => [
    ['Human rights are generally described as:', ['Inherent, inalienable, and universal', 'Granted only by employers', 'Available only to voters', 'Limited to property owners'], 0],
    ['The Commission on Human Rights is a:', ['Constitutional independent office', 'Cabinet department', 'Private NGO', 'Local government unit'], 0],
  ],
  'Environment Management and Protection' => [
    ['Sustainable development aims to meet present needs without:', ['Compromising future generations\' ability to meet theirs', 'Using any natural resources', 'Local government involvement', 'Scientific research'], 0],
    ['An EIA is typically required for projects that may:', ['Significantly affect the environment', 'Only change office furniture', 'Hire temporary staff', 'Print flyers'], 0],
  ],
  'Word meaning' => [
    ['Benevolent most nearly means:', ['Kind', 'Angry', 'Confused', 'Lazy'], 0],
    ['Scarce most nearly means:', ['Limited', 'Abundant', 'Colorful', 'Silent'], 0],
    ['Diligent most nearly means:', ['Hardworking', 'Careless', 'Rude', 'Lucky'], 0],
    ['Obsolete most nearly means:', ['Outdated', 'Brand new', 'Popular', 'Accurate'], 0],
  ],
  'Sentence completion' => [
    ['She studied hard _____ she wanted to pass the exam.', ['because', 'although', 'unless', 'despite'], 0],
    ['Neither the manager nor the staff _____ ready.', ['was', 'were', 'be', 'are being'], 0],
    ['If it rains tomorrow, the game _____.', ['will be postponed', 'is postpone', 'postponed', 'postpone'], 0],
  ],
  'Error recognition' => [
    ['Choose the sentence with NO error:', ['She has already finished the report.', 'She have already finished the report.', 'She has already finish the report.', 'She already have finished the report.'], 0],
    ['Which sentence is grammatically correct?', ['The data are being reviewed by the team.', 'The data is being review by the team.', 'The data are being review by the team.', 'The data is being reviewing by the team.'], 0],
  ],
  'Sentence structure' => [
    ['A simple sentence contains:', ['One independent clause', 'Two dependent clauses only', 'No verb', 'Only a phrase'], 0],
    ['Which is a compound sentence?', ['I studied, and I rested.', 'Studying hard for the exam.', 'When I arrived.', 'Because it rained.'], 0],
  ],
  'Paragraph organization' => [
    ['The topic sentence usually:', ['States the main idea of the paragraph', 'Lists unrelated facts only', 'Ends every essay', 'Replaces the conclusion'], 0],
    ['Coherence in a paragraph means ideas are:', ['Logically connected', 'Randomly arranged', 'All one-word answers', 'Never supported'], 0],
  ],
  'Reading comprehension' => [
    ['After reading a passage, the best way to find the main idea is to ask:', ['What is the passage mostly about?', 'How many commas are used?', 'Who printed the page?', 'What font size is used?'], 0],
    ['An inference is a conclusion that is:', ['Reasonable based on evidence in the text', 'Copied word-for-word only', 'Always stated in the title', 'Impossible to support'], 0],
  ],
  'Word analogy' => [
    ['Doctor is to hospital as teacher is to:', ['School', 'Patient', 'Medicine', 'Stethoscope'], 0],
    ['Book is to reading as fork is to:', ['Eating', 'Writing', 'Sleeping', 'Running'], 0],
    ['Hot is to cold as day is to:', ['Night', 'Noon', 'Sun', 'Light'], 0],
    ['Pen is to writer as brush is to:', ['Painter', 'Pilotist', 'Chef', 'Pilot'], 0],
  ],
  'Symbolic logic / abstract reasoning' => [
    ['If all A are B, and all B are C, then all A are:', ['C', 'Not C', 'Only A', 'Unknown with no relation'], 0],
    ['Which comes next in the sequence: 2, 4, 8, 16, ___?', ['32', '18', '20', '24'], 0],
    ['Which does not belong: Circle, Square, Triangle, Banana?', ['Banana', 'Circle', 'Square', 'Triangle'], 0],
    ['If TODAY is coded as UPEBZ, then NEXT is coded by shifting each letter +1. What is NEXT?', ['OFYU', 'MDWS', 'NEWT', 'OEYU'], 0],
  ],
  'Identifying assumptions and drawing conclusions' => [
    ['Statement: All civil servants must be honest. Assumption most needed:', ['Honesty is required in public service', 'All civil servants are already rich', 'Exams are unnecessary', 'Honesty cannot be taught'], 0],
    ['If no reptiles are mammals, and all lizards are reptiles, then:', ['No lizards are mammals', 'All lizards are mammals', 'Some mammals are lizards', 'All reptiles are lizards'], 0],
  ],
  'Data interpretation' => [
    ['A bar graph shows City A: 40, City B: 60. City B is what percent of City A?', ['150%', '50%', '66%', '120%'], 0],
    ['If a pie chart gives 25% to Category X of a 200 total, Category X equals:', ['50', '25', '75', '100'], 0],
    ['Sales rose from 80 to 100. The percent increase is:', ['25%', '20%', '80%', '125%'], 0],
  ],
  'Basic operations' => [
    ['15 + 27 = ?', ['42', '32', '52', '41'], 0],
    ['96 ÷ 8 = ?', ['12', '8', '16', '18'], 0],
    ['7 × 9 = ?', ['63', '56', '72', '64'], 0],
    ['100 − 37 = ?', ['63', '73', '67', '53'], 0],
  ],
  'Number sequence' => [
    ['Find the next number: 3, 6, 9, 12, ___', ['15', '14', '16', '18'], 0],
    ['Find the next number: 5, 10, 20, 40, ___', ['80', '60', '45', '50'], 0],
    ['Find the missing number: 2, 5, 10, 17, ___', ['26', '24', '20', '22'], 0],
  ],
  'Word problems' => [
    ['A jeepney fare is ₱13. For 4 passengers paying cash only, total is:', ['₱52', '₱48', '₱56', '₱40'], 0],
    ['A worker earns ₱800/day for 5 days. Total earnings:', ['₱4,000', '₱3,200', '₱4,800', '₱2,400'], 0],
    ['A shirt costs ₱500 with 10% discount. Sale price is:', ['₱450', '₱400', '₱490', '₱550'], 0],
  ],
  'Filing' => [
    ['In alphabetical filing, which name comes first?', ['Garcia, Ana', 'Santos, Ben', 'Reyes, Carlo', 'Torres, Dian'], 0],
    ['Which should be filed before "Lopez"?', ['Lim', 'Luna', 'Luz', 'Lyons'], 0],
  ],
  'Spelling' => [
    ['Choose the correctly spelled word:', ['Accommodation', 'Acommodation', 'Accomodation', 'Acomodation'], 0],
    ['Choose the correctly spelled word:', ['Bureaucracy', 'Beaurocracy', 'Bureacracy', 'Bureaukracy'], 0],
    ['Choose the correctly spelled word:', ['Separate', 'Seperate', 'Seperete', 'Separete'], 0],
  ],
];

$n = 0;
foreach ($bank as $subName => $items) {
  $sub = Subcategory::where('name', $subName)->first();
  if (!$sub) { echo "MISSING_SUB $subName\n"; continue; }
  foreach ($items as [$stem, $options, $correct]) {
    // create multiple copies so pool builder quotas can be met
    for ($copy = 1; $copy <= 8; $copy++) {
      Question::create([
        'subcategory_id' => $sub->id,
        'language' => 'English',
        'stem' => $copy === 1 ? $stem : ($stem . " (variant $copy)"),
        'options' => $options,
        'correct_option' => $correct,
        'explanation' => 'Local practice item for Docker Hiraya. Replace with Gemini/admin bank later.',
        'created_by' => $user->id,
        'status' => 'active',
      ]);
      $n++;
    }
  }
}

Cache::forget('questions.active');
Cache::forget('categories.tree');
echo "CREATED=$n ACTIVE=" . Question::where('status','active')->count() . "\n";
