import ProfileForm from "../components/profile/ProfileForm";

const ProfilePage = () => {
    return (
        <div className="container mx-auto py-8">
            <h1 className="text-3xl font-bold mb-6">
                Edit Profile
            </h1>

            <ProfileForm />
        </div>
    );
};

export default ProfilePage;