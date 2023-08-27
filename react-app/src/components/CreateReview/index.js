import { useState } from "react";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import * as reviewActions from '../../store/review';
import './CreateReview.css';

export default function CreateReview({ spotId }) {
    const dispatch = useDispatch();
    const { closeModal } = useModal();
    const [review, setReview] = useState('');
    const [stars, setStars] = useState(0);
    const [hover, setHover] = useState(null);
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newReview = {
            review,
            stars
        };
        const returnFromThunk = reviewActions.createReview(newReview, spotId);
        return dispatch(returnFromThunk).then(() => {
            dispatch(reviewActions.allReviews(spotId));
            closeModal();
        }).catch(async (res) => {
            const data = await res.json();
            if (data && data.errors) {
                setErrors(data.errors)
            }
        });
    };

    return (
        <>
            <div className='reviewModal'>
                <h1>How was your meal?</h1>
                <form onSubmit={handleSubmit}>
                    {errors.message && <p>{errors.message}</p>}
                    <textarea
                        id='reviewTextarea'
                        type='text'
                        value={review}
                        onChange={(e) => setReview(e.target.value)}
                        placeholder='Leave your review here...' />
                    <div id='stars'>
                        {[...Array(5)].map((star, index) => {
                            const currentRating = index + 1;
                            return (
                                <label>
                                    <input
                                        className='starsRadio'
                                        type='radio'
                                        value={currentRating}
                                        onClick={(e) => setStars(e.target.value)}
                                    />
                                    <i class="fa-solid fa-star"
                                        id='starMenu'
                                        color={currentRating <= (hover || stars) ? '#fefe33' : '#e4e5e9'}
                                        onMouseEnter={() => setHover(currentRating)}
                                        onMouseLeave={() => setHover(null)}></i>
                                </label>
                            )
                        })} Stars
                    </div>
                    <button type='submit' className='signupSubmit' disabled={review.length < 10 || stars === 0}>Submit Your Review</button>
                </form>
            </div>
        </>
    )
}
